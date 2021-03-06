#!/usr/bin/env python3
import os
import requests
import hmac
import hashlib
import base64

from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.core.cache import cache
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .models import SalesforceOrg, ClientOrg, Token
from .serializers import (
    SalesforceOrgSerializer,
    ClientOrgSerializer,
    SalesforceTokenDataSerializer,
)
from .utils import ClientsUtils
from redditors.models import Redditor
from redditors.serializers import RedditorSerializer
from redditors.utils import RedditorsUtils
from api.permissions import MyOauthConfirmPermission
from api.token_authentication import MyTokenAuthentication
from subreddits.utils import SubredditsUtils
from api.utils import Utils

logger = Utils.init_logger(__name__)


class ClientsInfo(APIView):
    # TODO get all clients info from database, this is only permitted for session auth.

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        pass


class ClientOauth(APIView):
    """
    API endpoint that initiates the Reddit Account oauth flow
    """

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth request =>')

        # Create a valid state integer and save it to cache
        state = Utils.save_valid_state_in_cache('oauth')
        logger.debug(f'Saving oauth_{state} in cache with status pending')

        # Obtain authorization URL
        reddit = reddit = Utils.get_reddit_instance()
        # scopes = ['*'] All OAuth scopes available
        scopes = [
            'edit',
            'history',
            'identity',
            'mysubreddits',
            'read',
            'submit',
            'subscribe',
            'vote',
        ]
        auth_url = reddit.auth.url(scopes, state)
        logger.debug(f'Reddit auth url: {auth_url}')

        return Response(
            {'oauth_url': auth_url, 'state': state}, status=status.HTTP_200_OK
        )


class ClientOauthCallback(APIView):
    """
    API endpoint that handles the callback from Reddit Oauth flow
    """

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth callback =>')

        error_msg = None
        status_code = 200
        state = request.query_params.get('state')
        logger.debug(f'state in request: {state}')
        if not state:
            error_msg = 'state param not found.'
            status_code = status.HTTP_400_BAD_REQUEST
        elif not cache.has_key(f'oauth_{state}'):
            error_msg = 'Invalid or expired state.'
            status_code = status.HTTP_412_PRECONDITION_FAILED
        else:
            logger.info(f'State verified successfully!')

            # Check for error in query params
            oauth_error = request.query_params.get('error')
            if oauth_error:
                error_msg = oauth_error
                status_code = status.HTTP_417_EXPECTATION_FAILED
            else:
                code = request.query_params.get('code')
                logger.debug(f'code in request: {code}')
                if not code:
                    error_msg = 'code param not found.'
                    status_code = status.HTTP_400_BAD_REQUEST
                else:
                    cache.set(
                        f'oauth_{state}',
                        {'status': 'accepted', 'status_code': 200, 'code': code},
                        900,
                    )
                    logger.info('Reddit oauth code saved in cache succesfully!')

        # Update cache oauth_state with error msg
        if error_msg:
            logger.error(error_msg)
            cache.set(
                f'oauth_{state}',
                {'status': 'error', 'status_code': status_code, 'detail': error_msg},
                900,
            )
        # Redirect to generic Salesforce login domain
        return HttpResponse(
            ''' <script type="text/javascript">
                    window.close();
                </script>'''
        )


class ClientOauthConfirmation(APIView):
    """
    API endpoint to check oauth status for a Salesforce Org (GET) 
    and handle the confirmation of a Reddit account for some Salesforce org (POST)
    """

    permission_classes = [MyOauthConfirmPermission]

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth status =>')

        state = request.query_params.get('state')
        # Get oauth_data from cache using state
        oauth_data = cache.get(f'oauth_{state}')
        oauth_status = oauth_data['status']
        if oauth_status == 'pending':
            return Response(
                data={'detail': 'Authorization still pending.'},
                status=status.HTTP_202_ACCEPTED,
            )
        elif oauth_status == 'accepted' or oauth_status == 'error':
            response_data = {'result': oauth_status}
            response_data['detail'] = (
                lambda x, y: 'Authorization complete.' if x == 'accepted' else y
            )(
                oauth_status,
                oauth_data['detail'] if 'detail' in oauth_data.keys() else None,
            )

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise exceptions.APIException(
                detail={'detail': 'Invalid status detected'},
                code=status.HTTP_501_NOT_IMPLEMENTED,
            )

    def post(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Reddit Oauth confirmation =>')

        # First validated request.data and save the SalesforceOrg object
        org = SalesforceOrg.objects.get_or_none(org_id=request.data.get('org_id'))
        serializer = SalesforceOrgSerializer(instance=org, data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        logger.debug(f'Org data => {org}')

        state = request.query_params.get('state')
        # Get refresh token from cache
        oauth_data = cache.get(f'oauth_{state}')
        # Delete from cache after getting the data needed
        cache.delete(f'oauth_{state}')

        # Get the reddit code and generate the refresh_token
        reddit_code = oauth_data['code']
        reddit = Utils.get_reddit_instance()
        if reddit_code == 'dummy':
            refresh_token = None
            redditor_data = RedditorsUtils.get_dummy_redditor_data()
            redditor_id = redditor_data['id']
        else:
            refresh_token = reddit.auth.authorize(reddit_code)
            # Get the redditor data from API
            api_redditor = reddit.user.me()
            redditor_id = api_redditor.id
            redditor_data = RedditorsUtils.get_redditor_data(api_redditor)

        # Create or update redditor object for this client
        redditor = Redditor.objects.get_or_none(id=redditor_id)
        serializer = RedditorSerializer(instance=redditor, data=redditor_data)
        serializer.is_valid(raise_exception=True)
        redditor = serializer.save()
        logger.info(repr(redditor))
        redditor_data = serializer.data

        # Finally save the client org object
        client_org = ClientOrg.objects.get_or_none(
            redditor_id=redditor.id, salesforce_org_id=org.org_id
        )
        serializer = ClientOrgSerializer(
            instance=client_org,
            data={
                'connected_at': now(),
                'reddit_token': refresh_token,
                'is_active': True,
            },
        )
        serializer.is_valid(raise_exception=True)
        client_org = serializer.save(salesforce_org=org, redditor=redditor)

        # Create a random token for this client_org
        # This token will be used to authenticate the client org for all future requests
        token = Token.objects.get_or_none(client_org_id=client_org.id)
        if token:
            token.delete()
        token = Token.objects.create(client_org=client_org)
        logger.debug(f'Bearer token generated: {token.key}')

        subreddits = []
        if reddit_code != 'dummy':
            for sub in reddit.user.subreddits():
                subreddits.append(SubredditsUtils.get_subreddit_data_simple(sub))

        # Return redditor data + subscriptions + token generated
        redditor_data.update(subscriptions=subreddits, bearer_token=token.key)
        return Response(redditor_data, status=status.HTTP_201_CREATED)


class Client(APIView):
    """
    API endpoint to get authenticated Reddit account info.
    GET request returns the redditor data.
    DELETE request revokes reddit authorization and deletes oauth token from database
    Expects a valid bearer token in the Authorization header.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Client information request =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)

        subreddits = []
        if reddit.read_only:
            redditor_data = RedditorsUtils.get_dummy_redditor_data()
            redditor_id = redditor_data['id']
        else:
            # Get the current authenticated reddit user data
            api_redditor = reddit.user.me()
            redditor_id = api_redditor.id
            redditor_data = RedditorsUtils.get_redditor_data(api_redditor)
            for sub in reddit.user.subreddits():
                subreddits.append(SubredditsUtils.get_subreddit_data_simple(sub))

        # Create or update redditor object for this client
        redditor = Redditor.objects.get_or_none(id=redditor_id)
        serializer = RedditorSerializer(instance=redditor, data=redditor_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        redditor_data = serializer.data

        redditor_data.update(subscriptions=subreddits)
        return Response(data=redditor_data, status=status.HTTP_200_OK)

    def delete(self, request, Format=None):
        """
        Method to disconnect a Salesforce Org Client. Revokes access token from Reddit and
        deletes oauth token in database changing the Client Org to inactive status in the process
        """
        logger.info('-' * 100)
        logger.info('Client Reddit access token revoke =>')

        # If the request is authenticated correctly by the bearer token then I can get
        # the client_org from the request.user. Return tuple from TokenAuthentication:
        # (request.user, request.auth) = (client_org, bearer_token)

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        try:
            reddit._core._authorizer.revoke()
            logger.info('Reddit access token revoked succesfully.')
        except Exception as ex:
            logger.error(f'Error revoking access. Exception raised: {repr(ex)}.')

        # Now I need to delete the oauth_token from database and change the status to inactive
        _, salesforce_org_name = ClientsUtils.get_salesforce_org_id_name(client_org)
        logger.info(
            f'Deleting Reddit access token for org \'{salesforce_org_name}\' '
            'and changing status to inactive for client.'
        )
        serializer = ClientOrgSerializer(
            instance=client_org,
            data={'disconnected_at': now(), 'reddit_token': None, 'is_active': False},
        )
        serializer.is_valid(raise_exception=True)
        client_org = serializer.save()

        bearer_token = request.auth
        logger.debug(repr(bearer_token))
        bearer_token.delete()

        return Response(
            data={'detail': 'Account disconnected succesfully.'},
            status=status.HTTP_200_OK,
        )


class SalesforceOauth(APIView):
    """
    API endpoint that initiates a Salesforce org OAuth using the connected app credentials.
    """

    # This endpoint is only usable for orgs that already
    # have a bearer token from the reddit oauth flow
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    endpoint_url = 'https://login.salesforce.com/services/oauth2/authorize'
    redirect_uri = f'{os.environ.get("DOMAIN_URL")}/clients/salesforce_oauth_callback'
    client_id = os.environ.get('CONNECTED_APP_KEY')
    is_permanent = True

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Client Salesforce OAuth request =>')

        # Get the org_id from the request, I need to save it in cache because the callback
        # cannnot have a Bearer token Authorization header
        client_org = request.user
        # Save valid state integer in cache with the org_id linked to the client_org
        state = Utils.save_valid_state_in_cache(
            'salesforce_oauth', client_org.salesforce_org_id
        )
        logger.debug(f'Saving salesforce_oauth_{state} in cache with status pending')

        oauth_url = Utils.make_url_with_params(
            self.endpoint_url,
            response_type='code',
            client_id=self.client_id,
            prompt='consent',
            redirect_uri=self.redirect_uri,
            scope='full refresh_token',
            state=state,
        )
        return Response(
            {'oauth_url': oauth_url, 'state': state}, status=status.HTTP_200_OK
        )


class SalesforceOauthCallback(APIView):
    """
    API endpoint to handle the callback from Salesforce oauth flow
    """

    endpoint_url = 'https://login.salesforce.com/services/oauth2/token'
    redirect_uri = f'{os.environ.get("DOMAIN_URL")}/clients/salesforce_oauth_callback'
    grant_type = 'authorization_code'

    client_id = os.environ.get('CONNECTED_APP_KEY')
    client_secret = os.environ.get('CONNECTED_APP_SECRET')

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('Client Salesforce OAuth callback =>')

        error_msg = None
        status_code = 200
        redirect_instance = 'https://login.salesforce.com/'
        state = request.query_params.get('state')
        if not state:
            error_msg = 'state param not found.'
            status_code = status.HTTP_400_BAD_REQUEST
        elif not cache.has_key(f'salesforce_oauth_{state}'):
            error_msg = 'Invalid or expired state.'
            status_code = status.HTTP_412_PRECONDITION_FAILED
        else:
            logger.info(f'State verified successfully!')

            # First check for error and error_description params
            error = request.query_params.get('error')
            if error:
                error_msg = (
                    request.query_params.get('error_description')
                    if 'error_description' in request.query_params
                    else 'access denied.'
                )
                status_code = status.HTTP_417_EXPECTATION_FAILED
            else:
                code = request.query_params.get('code')
                if not code:
                    error_msg = 'code param not found.'
                    status_code = status.HTTP_400_BAD_REQUEST
                else:
                    # Get org_id saved in cache
                    oauth_state_data = cache.get(f'salesforce_oauth_{state}')
                    org_id = oauth_state_data['org_id']
                    cache.set(
                        f'salesforce_oauth_{state}',
                        {'status': 'accepted', 'code': code, 'org_id': org_id},
                        900,
                    )
                    logger.info('Salesforce oauth code saved in cache succesfully!')

                    # Create request to ask for access_token
                    req = self._make_token_request(code)
                    logger.debug(req.status_code)

                    if req.status_code == 200:
                        logger.info('Token request successful!')
                        response_json = req.json()
                        logger.debug(f'Response JSON: {response_json}')

                        if self._signature_verifies(response_json):
                            logger.info('Signature verified succesfully!')
                            # Save the instance_url and access token here...
                            instance_url = response_json['instance_url']
                            access_token = response_json['access_token']
                            refresh_token = response_json['refresh_token']

                            org = SalesforceOrg.objects.get_or_none(org_id=org_id)
                            logger.debug(f'Org data: {org}')
                            if org:
                                serializer = SalesforceOrgSerializer(
                                    instance=org,
                                    data={
                                        'instance_url': instance_url,
                                        'access_token': access_token,
                                        'refresh_token': refresh_token,
                                    },
                                    partial=True,
                                )
                                serializer.is_valid(raise_exception=True)
                                serializer.save()
                            else:
                                error_msg = (
                                    f'Org with id: {org_id} not found in database.'
                                )
                                status_code = status.HTTP_406_NOT_ACCEPTABLE

                            redirect_instance = instance_url
                        else:
                            error_msg = 'Invalid signature provided. The identity URL may be corrupted'
                            status_code = status.HTTP_401_UNAUTHORIZED
                    else:
                        error_msg = req.text
                        status_code = status.HTTP_417_EXPECTATION_FAILED

        # Update cache oauth_state with error msg
        if error_msg:
            logger.error(error_msg)
            cache.set(
                f'salesforce_oauth_{state}',
                {'status': 'error', 'status_code': status_code, 'detail': error_msg},
                900,
            )
        # Redirect to the instance_url if ok, else to generic Salesforce login
        return redirect(redirect_instance)

    def _make_token_request(self, code):
        # Create Authorization header as Basic Encode64(client_id:client_secret)
        basic_auth_encoded_bytes = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')
        )
        basic_auth_encoded_str = str(basic_auth_encoded_bytes, 'utf-8')
        headers = {
            'Authorization': f'Basic {basic_auth_encoded_str}',
            'Accept': 'application/json',
        }
        payload = {
            'grant_type': self.grant_type,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }

        return requests.post(self.endpoint_url, headers=headers, params=payload)

    def _signature_verifies(self, response_json):
        # Here I need to verify the signature in the json
        # It's a Base64-encoded HMAC-SHA256 containing the concatened
        # id and issued_at values. The key is the client_secret
        identity_url = response_json['id']
        issued_at = response_json['issued_at']
        digest = hmac.new(
            self.client_secret.encode('utf-8'),
            msg=f'{identity_url}{issued_at}'.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).digest()
        generated_signature = base64.b64encode(digest).decode()

        return response_json['signature'] == generated_signature


class SalesforceToken(APIView):
    """
    API endpoints to receive and revoke Salesforce access tokens
    """

    # This endpoints are only usable for orgs that already
    # have a bearer token from the reddit oauth flow
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]
    revoke_endpoint_url = 'https://login.salesforce.com/services/oauth2/revoke'

    def post(self, request, Format=None):
        """
        API endpoint that recieves an access token and instance url of a Salesforce org to connect
        this app with the org from the url. The access token is the one generated with sfdx.
        """
        logger.info('-' * 100)
        logger.info('Client Salesforce Token request =>')

        # Check if the data passed is acceptable with the custom serializer
        serializer = SalesforceTokenDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # First validated request.data and save the SalesforceOrg object
        org_id = request.user.salesforce_org_id
        org = SalesforceOrg.objects.get_or_none(org_id=org_id)
        if not org:
            return Response(
                data={
                    'status': 'error',
                    'detail': f'Salesforce org with id: {org_id} not found in database.',
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SalesforceOrgSerializer(
            instance=org, data=validated_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        logger.debug(f'Org data => {org}')

        return Response(
            data={
                'detail': 'Salesforce org access token and instance url updated succesfully.'
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, Format=None):
        """
        API endpoint that revokes the oauth access token for a Salesforce org according to the
        Authorization bearer token.
        """
        logger.info('-' * 100)
        logger.info('Client Salesforce revoke token =>')

        org_id = request.user.salesforce_org_id
        org = SalesforceOrg.objects.get_or_none(org_id=org_id)
        if not org:
            return Response(
                data={
                    'status': 'error',
                    'detail': f'Salesforce org with id: {org_id} not found in database.',
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        refresh_token = org.refresh_token
        # Just delete the tokens from the org record
        org.access_token = None
        org.refresh_token = None
        org.save()

        response_data = {
            'detail': f'Oauth access token revoked for Salesforce org with id: {org_id}.'
        }
        if refresh_token:
            # Now call Salesforce oauth revoke endpoint
            req = self._make_revoke_request(refresh_token)
            response_text = req.text
            if req.status_code == 200:
                response_data['revoke_result'] = 'Oauth token revoked successfully.'
            else:
                logger.debug(f'Error trying to revoke oauth token: {response_text}')
                response_data['revoke_result'] = f'{req.status_code}:{response_text}'
        else:
            response_data['revoke_result'] = 'No refresh token found to revoke.'

        return Response(data=response_data, status=status.HTTP_200_OK)

    def _make_revoke_request(self, refresh_token):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'token': refresh_token}
        return requests.post(self.revoke_endpoint_url, headers=headers, data=payload)
