#!/usr/bin/env python3
import os
import random
from pprint import pprint

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils.timezone import now

from .models import SalesforceOrg, ClientOrg, Token
from .serializers import SalesforceOrgSerializer, ClientOrgSerializer
from redditors.models import Redditor
from redditors.serializers import RedditorSerializer
from herokuredditapi.permissions import MyOauthConfirmPermission
from herokuredditapi.tokenauthentication import MyTokenAuthentication

from herokuredditapi.utils import utils
logger = utils.init_logger(__name__)


class ClientOauthView(APIView):
    """
    API endpoint that initiates the Reddit Account oauth flow
    """

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit New OAuth request...')

        state = str(random.randint(0, 65536))
        while cache.has_key(state):
            state = str(random.randint(0, 65536))
        cache.set(f'oauth_{state}', {'status': 'pending'})
        logger.debug(f'Saving oauth_{state} in cache with status pending')

        # Obtain authorization URL
        reddit = reddit = utils.get_reddit_instance()
        # scopes = ['identity', 'mysubreddits', 'read', 'subscribe', 'vote']
        auth_url = reddit.auth.url(['*'], state, 'permanent')
        logger.debug(f'Reddit auth url: {auth_url}')

        return Response({'oauth_url': auth_url, 'state': state}, status=status.HTTP_200_OK)


class ClientOauthCallbackView(APIView):
    """
    API endpoint that handles the callback from Reddit Oauth flow
    """

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth callback...')

        state = request.query_params.get('state')
        logger.debug(f'state in request: {state}')
        if not state:
            raise exceptions.ParseError(
                detail={'detail': 'state param not found.'})

        if cache.has_key(f'oauth_{state}'):
            logger.info(f'State verified successfully!')

            # Check for error in query params
            oauth_error = request.query_params.get('error')
            if oauth_error:
                cache.set(f'oauth_{state}', {
                          'status': 'error', 'detail': oauth_error})
                raise exceptions.PermissionDenied({'detail': oauth_error})

            code = request.query_params.get('code')
            logger.debug(f'code in request: {code}')
            if not code:
                raise exceptions.ParseError(
                    detail={'detail': 'code param not found.'})

            cache.set(f'oauth_{state}', {'status': 'accepted', 'code': code})
            logger.info('Reddit oauth code saved in cache succesfully!')
            # Return a response with 200:OK here...
            return Response({'detail': 'Oauth code saved successfully.'}, status=status.HTTP_200_OK)
        else:
            msg = 'Invalid or expired state.'
            logger.error(msg)
            cache.set(f'oauth_{state}', {'status': 'error', 'detail': msg})
            raise exceptions.AuthenticationFailed(detail={'detail': msg})


class ClientOauthConfirmationView(APIView):
    """
    API endpoint to check oauth status for a Salesforce Org (GET) 
    and handle the confirmation of a Reddit account for some Salesforce org (POST)
    """
    permission_classes = [MyOauthConfirmPermission]

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth status ping...')

        state = request.query_params.get('state')
        # Get oauth_data from cache using state
        oauth_data = cache.get(f'oauth_{state}')
        oauth_status = oauth_data['status']
        if oauth_status == 'pending':
            return Response(data={'detail': 'Authorization still pending.'},
                            status=status.HTTP_202_ACCEPTED)
        elif oauth_status == 'accepted' or oauth_status == 'error':
            response_data = {'result': oauth_status}
            response_data['detail'] = (
                lambda x, y: 'Authorization complete.' if x == 'accepted' else y
            )(oauth_status, oauth_data['detail'] if 'detail' in oauth_data.keys() else None)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise exceptions.APIException(
                detail={'detail': 'Invalid status detected'}, code=status.HTTP_501_NOT_IMPLEMENTED)

    def post(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth confirmation post...')

        state = request.query_params.get('state')
        # Get refresh token from cache
        oauth_data = cache.get(f'oauth_{state}')
        # Delete from cache after getting the data needed
        cache.delete(f'oauth_{state}')
        # Get the reddit code and generate the refresh_token
        reddit_code = oauth_data['code']
        reddit = utils.get_reddit_instance()
        refresh_token = reddit.auth.authorize(reddit_code)
        # Get the redditor data from API
        api_redditor = reddit.user.me()
        pprint(vars(api_redditor))

        # Create or update redditor object for this client
        redditor = Redditor.objects.get_or_none(id=api_redditor.id)
        serializer = RedditorSerializer(
            instance=redditor, data=utils.get_redditor_data(api_redditor))
        serializer.is_valid(raise_exception=True)
        redditor = serializer.save()
        logger.info(repr(redditor))
        redditor_data = serializer.data

        # Then save the Salesforce org data
        org = SalesforceOrg.objects.get_or_none(
            org_id=request.data['org_id'])
        serializer = SalesforceOrgSerializer(
            instance=org, data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        logger.debug(org)

        # Finally save the client org object
        client_org = ClientOrg.objects.get_or_none(
            redditor_id=redditor.id, salesforce_org_id=org.org_id)
        serializer = ClientOrgSerializer(instance=client_org,
                                         data={'connected_at': now(),
                                               'reddit_token': refresh_token,
                                               'is_active': True})
        serializer.is_valid(raise_exception=True)
        client_org = serializer.save(salesforce_org=org, redditor=redditor)

        # Create a random token for this client_org
        # This token will be used to authenticate the client org for all future requests
        token = Token.objects.get_or_none(client_org_id=client_org.id)
        if token:
            token.delete()
        token = Token.objects.create(client_org=client_org)
        logger.debug(token.key)

        reddit_user = reddit.user
        subreddits = []
        for sub in reddit_user.subreddits():
            subreddits.append(
                {'id': sub.id, 'display_name': sub.display_name,
                 'public_description': sub.public_description,
                 'subscribers': sub.subscribers})

        # Return redditor data + subscriptions + token generated
        redditor_data.update(subscriptions=subreddits, bearer_token=token.key)
        return Response(redditor_data, status=status.HTTP_201_CREATED)

class ClientView(APIView):
    """
    API endpoint to get authenticated Reddit account info.
    GET request returns the redditor data.
    Expects a valid bearer token in the Authorization header.
    """
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Get redditor data for authenticated reddit account...')

        # If the request is authenticated correctly by the bearer token then I can get
        # the client_org from the request.user. Return tuple from TokenAuthentication:
        # (request.user, request.auth) = (client_org, bearer_token)
        client_org = request.user
        client_org.new_client_request()
        reddit = utils.get_reddit_instance(token=client_org.reddit_token)

        # Get the current authenticated reddit user data
        reddit_user = reddit.user
        subreddits = []
        for sub in reddit_user.subreddits():
            subreddits.append(
                {'id': sub.id, 'display_name': sub.display_name,
                 'public_description': sub.public_description,
                 'subscribers': sub.subscribers})

        api_redditor = reddit_user.me()
        # Create or update redditor object for this client
        redditor = Redditor.objects.get_or_none(id=api_redditor.id)
        serializer = RedditorSerializer(
            instance=redditor, data=utils.get_redditor_data(api_redditor))
        serializer.is_valid(raise_exception=True)
        redditor = serializer.save()
        redditor_data = serializer.data

        redditor_data.update(subscriptions=subreddits)
        return Response(data=redditor_data, status=status.HTTP_200_OK)

class ClientDisconnectView(APIView):
    """
    API endpoint to disconnect a Salesforce Org Client. DELETE request that deletes oauth token and 
    changes the Client Org to inactive status.
    """
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Account disconnect...')

        # If the request is authenticated correctly by the bearer token then I can get
        # the client_org from the request.user. Return tuple from TokenAuthentication:
        # (request.user, request.auth) = (client_org, bearer_token)
        client_org = request.user
        serializer = ClientOrgSerializer(instance=client_org,
                                         data={'disconnected_at': now(),
                                               'reddit_token': None,
                                               'is_active': False})
        serializer.is_valid(raise_exception=True)
        client_org = serializer.save()

        bearer_token = request.auth
        logger.debug(repr(bearer_token))
        bearer_token.delete()

        return Response(data={'detail': 'Account disconnected succesfully.'},
                        status=status.HTTP_200_OK)

class ClientsView(APIView):
    """
    API endpoint to get all clients orgs, needs admin credentials...
    """
    # authentication_classes = [MyTokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get(self, request, Format=None):
    #     pass
