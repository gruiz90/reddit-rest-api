#!/usr/bin/env python3
import random
import logging
import colorlog
import os
import praw
import urllib
from datetime import datetime

from rest_framework.views import exception_handler
from rest_framework import exceptions
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from prawcore.exceptions import ResponseException

from clients.models import ClientOrg
from redditors.models import Redditor


def custom_json_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        data = {'error': {'code': response.status_code}}
        errors = []
        for field, value in response.data.items():
            value_str = str(value).replace('"', "'")
            errors.append(f'{field}: {value_str}')
        data['error']['messages'] = errors
        response.data = data
    return response


TESTING_MODE = os.environ.get('LOGLEVEL_DEBUG', False) == 'True'


class Utils(object):
    @staticmethod
    def init_logger(dunder_name) -> logging.Logger:
        log_format = (
            '%(asctime)s - '
            '%(name)s - '
            '%(lineno)d - '
            '%(funcName)s - '
            '%(levelname)s - '
            '%(message)s'
        )
        bold_seq = '\033[1m'
        colorlog_format = f'{bold_seq} ' '%(log_color)s ' f'{log_format}'
        colorlog.basicConfig(format=colorlog_format)
        logger = logging.getLogger(dunder_name)

        if TESTING_MODE:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        return logger

    @staticmethod
    def get_reddit_instance(token=None):
        if token:
            return praw.Reddit(
                client_id=os.environ.get('REDDIT_CLIENT_ID'),
                client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                user_agent=os.environ.get('REDDIT_USER_AGENT'),
                refresh_token=token,
            )
        else:
            return praw.Reddit(
                client_id=os.environ.get('REDDIT_CLIENT_ID'),
                client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                user_agent=os.environ.get('REDDIT_USER_AGENT'),
                redirect_uri=f'{os.environ.get("DOMAIN_URL")}/clients/oauth_callback',
            )

    @staticmethod
    def new_client_request(auth_client):
        """
        Receives an auth_client instance from request.user and returns the authorized reddit instance
        ready to use if the token authentication was correct, or if there is a client org corresponding
        with the authorized session user. If no client_org is found then the reddit instance is read only.
        Arguments:
            auth_client {[ClientOrg | Django.AuthUser]} --
            [ClientOrg object with validated reddit_token | Django super user]
        """
        client_org = None
        session_auth = False
        if type(auth_client) is not ClientOrg:
            session_auth = True
            # Here I need to get a valid client org for the authenticated user, look for a redditor with
            # same name as the user and get the client_org object with this redditor if possible
            redditor = Redditor.objects.get_or_none(name=auth_client.username)
            if redditor:
                try:
                    client_org = (
                        ClientOrg.objects.filter(
                            redditor_id=redditor.id, is_active=True
                        )
                        .order_by('-connected_at')[0:1]
                        .get()
                    )
                except ObjectDoesNotExist:
                    # Just print this here...
                    print(
                        f'No client org found corresponding to username: {auth_client.username}'
                    )
        else:
            # If the request is authenticated correctly by the bearer token then I can get
            # the client_org from the request.user. Return tuple from TokenAuthentication:
            # (request.user, request.auth) = (client_org, bearer_token)
            client_org = auth_client

        if client_org:
            client_org.new_client_request()
            reddit = Utils.get_reddit_instance(token=client_org.reddit_token)
            # Here I need to check if the access token is actually alive
            # I can do a request to get the authenticated user data in a try/except
            try:
                reddit.user.me()
            except ResponseException as ex:
                if session_auth:
                    # In this case if the reddit token is not live then just use
                    # read only instance
                    return Utils.get_reddit_instance(), None
                else:
                    raise exceptions.AuthenticationFailed(
                        'Reddit access token authorization problem. '
                        'The user may need to re-authorize the app. '
                        f'Exception raised: {repr(ex)}.'
                    )

            # All cool, I can return the reddit instance and client_org tuple
            return reddit, client_org
        else:
            # Read only reddit instance when no client org found
            return Utils.get_reddit_instance(), None

    @staticmethod
    def save_valid_state_in_cache(key, org_id=None):
        state = str(random.randint(0, 65536))
        while cache.has_key(f'{key}_{state}'):
            state = str(random.randint(0, 65536))
        state_data = {'status': 'pending'}
        if org_id:
            state_data['org_id'] = org_id
        cache.set(f'{key}_{state}', state_data, 900)
        return state

    @staticmethod
    def make_url_with_params(path_url, **kwargs):
        return f'{path_url}?{urllib.parse.urlencode(kwargs)}'

    @staticmethod
    def validate_body_value(body):
        if body is None:
            raise exceptions.ParseError(
                detail={'detail': 'A body value must be provided in the json data.'}
            )
        if not isinstance(body, str):
            raise exceptions.ParseError(
                detail={
                    'detail': 'The body must contain the comment in a Markdown format.'
                }
            )
        return body
