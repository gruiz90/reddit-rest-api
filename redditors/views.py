#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from herokuredditapi.tokenauthentication import MyTokenAuthentication
from .models import Redditor
from .serializers import RedditorSerializer
from pprint import pprint

from herokuredditapi.utils import utils
logger = utils.init_logger(__name__)


class RedditorAccountView(APIView):
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
