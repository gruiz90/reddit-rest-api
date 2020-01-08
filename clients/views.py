#!/usr/bin/env python3
import os
import requests
import hmac
import hashlib
import base64
from pprint import pprint

from rest_framework.views import APIView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic.base import RedirectView

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
from subreddits.utils import SubredditsUtils
from redditors.utils import RedditorsUtils

from herokuredditapi.utils import Utils
logger = Utils.init_logger(__name__)


class ClientOauthView(APIView):
    """
    API endpoint that initiates the Reddit Account oauth flow
    """

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit New OAuth request...')

        # Create a valid state integer and save it to cache
        state = Utils.save_valid_state_in_cache('oauth')
        logger.debug(f'Saving oauth_{state} in cache with status pending')

        # Obtain authorization URL
        reddit = reddit = Utils.get_reddit_instance()
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

        error_msg = None
        state = request.query_params.get('state')
        logger.debug(f'state in request: {state}')
        if not state:
            error_msg = 'state param not found.'

        if not error_msg and not cache.has_key(f'oauth_{state}'):
            error_msg = 'Invalid or expired state.'
        else:
            logger.info(f'State verified successfully!')

            # Check for error in query params
            oauth_error = request.query_params.get('error')
            if oauth_error:
                error_msg = oauth_error

            if not error_msg:
                code = request.query_params.get('code')
                logger.debug(f'code in request: {code}')
                if not code:
                    error_msg = 'code param not found.'

                if not error_msg:
                    cache.set(f'oauth_{state}', {
                              'status': 'accepted', 'code': code})
                    logger.info(
                        'Reddit oauth code saved in cache succesfully!')
                    # Return a response with 200:OK here...
                    # return Response({'detail': 'Oauth code saved successfully.'}, status=status.HTTP_200_OK)

        # Update cache oauth_state with error msg
        if error_msg:
            logger.error(error_msg)
            cache.set(f'oauth_{state}', {
                      'status': 'error', 'detail': error_msg})
        # Redirect to generic Salesforce domain
        return redirect('https://login.salesforce.com/')


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

        # First validated request.data and save the SalesforceOrg object
        org = SalesforceOrg.objects.get_or_none(
            org_id=request.data.get('org_id'))
        serializer = SalesforceOrgSerializer(
            instance=org, data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        logger.debug(org)

        state = request.query_params.get('state')
        # Get refresh token from cache
        oauth_data = cache.get(f'oauth_{state}')
        # Delete from cache after getting the data needed
        cache.delete(f'oauth_{state}')
        # Get the reddit code and generate the refresh_token
        reddit_code = oauth_data['code']
        reddit = Utils.get_reddit_instance()
        refresh_token = reddit.auth.authorize(reddit_code)
        # Get the redditor data from API
        api_redditor = reddit.user.me()
        pprint(vars(api_redditor))

        # Create or update redditor object for this client
        redditor = Redditor.objects.get_or_none(id=api_redditor.id)
        serializer = RedditorSerializer(
            instance=redditor, data=RedditorsUtils.get_redditor_data(api_redditor))
        serializer.is_valid(raise_exception=True)
        redditor = serializer.save()
        logger.info(repr(redditor))
        redditor_data = serializer.data

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
            subreddits.append(SubredditsUtils.get_subreddit_data_simple(sub))

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

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit = Utils.new_client_request(request.user)

        # Get the current authenticated reddit user data
        reddit_user = reddit.user
        subreddits = []
        for sub in reddit_user.subreddits():
            subreddits.append(SubredditsUtils.get_subreddit_data_simple(sub))

        api_redditor = reddit_user.me()
        # Create or update redditor object for this client
        redditor = Redditor.objects.get_or_none(id=api_redditor.id)
        serializer = RedditorSerializer(
            instance=redditor, data=RedditorsUtils.get_redditor_data(api_redditor))
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
    pass


class SalesforceOauthView(RedirectView):
    """
    API endpoint that creates a Salesforce oauth url and redirects there
    """

    endpoint_url = 'https://login.salesforce.com/services/oauth2/authorize'
    redirect_uri = f'{os.environ.get("DOMAIN_URL")}/clients/salesforce_oauth_callback'
    client_id = os.environ.get('CONNECTED_APP_KEY')
    is_permanent = True

    def get_redirect_url(self, org_id):
        logger.info('-' * 100)
        logger.info('New Salesforce OAuth request...')
        logger.info(org_id)
        # Save valid state integer in cache
        state = Utils.save_valid_state_in_cache('salesforce_oauth', org_id)
        logger.debug(
            f'Saving salesforce_oauth_{state} in cache with status pending')

        oauth_url = Utils.make_url_with_params(self.endpoint_url, response_type='code',
                                               client_id=self.client_id,
                                               redirect_uri=self.redirect_uri, state=state)
        return oauth_url


class SalesforceOauthCallbackView(APIView):
    """
    API endpoint to handle the callback from Salesforce oauth flow
    """

    endpoint_url = 'https://login.salesforce.com/services/oauth2/token'
    redirect_uri = f'{os.environ.get("DOMAIN_URL")}/clients/salesforce_oauth_callback'
    grant_type = 'authorization_code'

    client_id = os.environ.get('CONNECTED_APP_KEY')
    client_secret = os.environ.get('CONNECTED_APP_SECRET')

    def get(self, request, Format=None):
        state = request.query_params.get('state')
        logger.debug(f'state in request: {state}')
        if not state:
            raise exceptions.ParseError(
                detail={'detail': 'state param not found.'})

        if cache.has_key(f'salesforce_oauth_{state}'):
            logger.info(f'State verified successfully!')

            code = request.query_params.get('code')
            logger.debug(f'code in request: {code}')
            if not code:
                raise exceptions.ParseError(
                    detail={'detail': 'code param not found.'})

            # Get org_id from cache
            oauth_state_data = cache.get(f'salesforce_oauth_{state}')
            org_id = oauth_state_data['org_id']
            cache.set(f'salesforce_oauth_{state}', {
                'status': 'accepted', 'code': code, 'org_id': org_id})
            logger.info('Salesforce oauth code saved in cache succesfully!')

            # Create Authorization header as Basic Encode64(client_id:client_secret)
            basic_auth_encoded_bytes = base64.b64encode(
                f'{self.client_id}:{self.client_secret}'.encode('utf-8'))
            basic_auth_encoded_str = str(basic_auth_encoded_bytes, 'utf-8')
            headers = {
                'Authorization': f'Basic {basic_auth_encoded_str}',
                'Accept': 'application/json'
            }
            logger.debug(headers)

            payload = {'grant_type': self.grant_type,
                       'redirect_uri': self.redirect_uri, 'code': code}

            r = requests.post(self.endpoint_url,
                              params=payload, headers=headers)
            logger.debug(r.url)
            logger.debug(r.status_code)
            logger.debug(r.text)

            if r.status_code == 200:
                logger.info('Token request successful!')
                response_json = r.json()
                repr(response_json)
                logger.debug(str(response_json))

                # Here I need to verify the signature in the json
                # It's a Base64-encoded HMAC-SHA256 containing the concatened
                # id and issued_at values. The key is the client_secret
                identity_url = response_json['id']
                issued_at = response_json['issued_at']
                digest = hmac.new(self.client_secret.encode('utf-8'), msg=f'{identity_url}{issued_at}'.encode('utf-8'),
                                  digestmod=hashlib.sha256).digest()
                generated_signature = base64.b64encode(digest).decode()
                logger.debug(f'Generated Signature: {generated_signature}')

                response_signature = response_json['signature']
                logger.debug(f'Signature: {response_signature}')

                if generated_signature == response_signature:
                    logger.info('Signature verified succesfully')
                    # Save the instance_url and access token here...
                    instance_url = response_json['instance_url']
                    access_token = response_json['access_token']

                    logger.debug(f'OrgId: {org_id}')
                    org = SalesforceOrg.objects.get_or_none(
                        org_id=org_id)
                    logger.debug(org)
                    if org:
                        serializer = SalesforceOrgSerializer(
                            instance=org, data={'instance_url': instance_url, 
                            'access_token': access_token}, partial=True)
                        try:
                            serializer.is_valid(raise_exception=True)
                            org = serializer.save()
                            logger.debug(org)
                        except Exception as ex:
                            logger.error(ex)
                    else:
                        return Response(data={'detail': f'Org with id: {org_id} not found in database.'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    return redirect(instance_url)
                else:
                    msg = 'Invalid signature provided. The identity URL may be corrupted'
                    logger.error(msg)
                    cache.set(f'salesforce_oauth_{state}', {
                        'status': 'error', 'detail': msg})
                    raise exceptions.AuthenticationFailed(
                        detail={'detail': msg})
            else:
                return Response(data={'detail': r.text},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            msg = 'Invalid or expired state.'
            logger.error(msg)
            cache.set(f'salesforce_oauth_{state}', {
                'status': 'error', 'detail': msg})
            raise exceptions.AuthenticationFailed(detail={'detail': msg})
