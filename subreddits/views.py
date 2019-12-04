#!/usr/bin/env python3
from .models import Subreddit
from .serializers import SubredditSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from herokuredditapi.tokenauthentication import MyTokenAuthentication
from .utils import sub_utils

from herokuredditapi.utils import utils
logger = utils.init_logger(__name__)


class ConnectSubreddit(APIView):
    """
    API endpoint to connects a Salesforce org client to a subreddit by the name.
    This creates a connection between the ClientOrg and Subreddit, subscribes the reddit user if not already
    and returns all the relevant data about the subreddit.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        """POST request that expects the subreddit name to connect the client to.
        Arguments:
                request {[type]} -- DRF Request object
                name {[string]} -- Subreddit name
        Keyword Arguments:
                Format {[string]} -- [description] (default: {None})
        """
        logger.info('-' * 100)
        logger.info('New connect subreddit request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        subreddit = sub_utils.get_sub_if_exists(name, reddit)
        if subreddit is None:
                raise exceptions.NotFound(
                    detail={'detail': f'No subreddit exists with the name: {name}.'})

        logger.info(f'Connecting to Subreddit {subreddit.name}')
        if not subreddit.user_is_subscriber:
            logger.info(
                'Client is not subscribed, so I need to subscribe him here..')
            subreddit.subscribe()
        logger.info(f'Client subscribed: {subreddit.user_is_subscriber}')

        # Get data I need from subreddit instance
        subreddit_data = sub_utils.get_subreddit_data(subreddit)

        # Here for now I'll just save the subreddit_data in a Subreddit Model object
        # But I need to enqueue this into a redis queue, send the data to user as fast as possible
        subreddit_obj = sub_utils.create_or_update(subreddit_data)
        # Add the client_org connection to the object
        subreddit_obj.clients.add(client_org)
        # Show info about the subreddit obj in the log
        logger.info(repr(subreddit_obj))

        return Response(subreddit_data, status=status.HTTP_201_CREATED)


class DisconnectSubreddit(APIView):
    """
    API endpoint to disconnect a Salesforce org client to a Subreddit by the name.
    This only removes the connection between the ClientOrg and the Subreddit if exists.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info('New disconnect subreddit request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        subreddit = reddit.subreddit(name)

        subreddit_obj = Subreddit.objects.get_or_none(id=subreddit.id)
        if subreddit_obj is None:
            raise exceptions.NotFound(
                detail={'detail': 'No subreddit found with the name provided to make the disconnection.'})
        # Remove the client connection from both sides
        subreddit_obj.clients.remove(client_org)
        client_org.subreddit_set.remove(subreddit_obj)

        return Response(data={'detail': 'Client disconnected subreddit succesfully.'},
                        status=status.HTTP_200_OK)


class SubredditView(APIView):
    """
    API endpoint to get the Subreddit data by the name provided.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info('New subreddit details request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        subreddit = sub_utils.get_sub_if_exists(name, reddit)
        if subreddit is None:
                raise exceptions.NotFound(
                    detail={'detail': f'No subreddit exists with the name: {name}.'})

        # Get data I need from subreddit instance
        subreddit_data = sub_utils.get_subreddit_data(subreddit)
        # Enqueue this in a redis queue job later
        sub_utils.create_or_update(subreddit_data)

        return Response(subreddit_data, status=status.HTTP_200_OK)


class SubredditSubscriptions(APIView):
    """
    API endpoint to get a list of subreddits subscriptions for the client.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info('New subreddit subscriptions details request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)

        reddit_user = reddit.user
        subreddits = []
        for sub in reddit_user.subreddits():
            subreddits.append(sub_utils.get_subreddit_data_simple(sub))

        return Response({'subscriptions': subreddits}, status=status.HTTP_200_OK)


class SubredditRules(APIView):
    """
    API endpoint to get the rules of a subreddit by name.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info('New subreddit get rules request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        subreddit = sub_utils.get_sub_if_exists(name, reddit)
        if subreddit is None:
                raise exceptions.NotFound(
                    detail={'detail': f'No subreddit exists with the name: {name}.'})

        return Response(subreddit.rules(), status=status.HTTP_200_OK)


class SubredditSubscribe(APIView):
    """
    API endpoint to subscribe a Salesforce org client to a subreddit by the name.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info('New subreddit subscribe request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        subreddit = sub_utils.get_sub_if_exists(name, reddit)
        if subreddit is None:
                raise exceptions.NotFound(
                    detail={'detail': f'No subreddit exists with the name: {name}.'})

        if not subreddit.user_is_subscriber:
            subreddit.subscribe()

        logger.info(f'Client subscribed: {subreddit.user_is_subscriber}')

        return Response({'detail': f'Client succesfully subscribed to {name}.'}, status=status.HTTP_200_OK)


class SubredditUnsubscribe(APIView):
    """
    API endpoint to unsubscribe a Salesforce org client from a subreddit by the name.
    """

    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info('New subreddit unsubscribe request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        subreddit = sub_utils.get_sub_if_exists(name, reddit)
        if subreddit is None:
                raise exceptions.NotFound(
                    detail={'detail': f'No subreddit exists with the name: {name}.'})

        if subreddit.user_is_subscriber:
            subreddit.unsubscribe()

        logger.info(f'Client subscribed: {subreddit.user_is_subscriber}')

        return Response({'detail': f'Client succesfully unsubscribed from {name}.'}, status=status.HTTP_200_OK)
