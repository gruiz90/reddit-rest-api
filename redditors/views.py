#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from herokuredditapi.tokenauthentication import MyTokenAuthentication
from .models import Redditor
from .serializers import RedditorSerializer
from .utils import RedditorsUtils
from subreddits.utils import SubredditsUtils

from herokuredditapi.utils import Utils
logger = Utils.init_logger(__name__)


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


class RedditorView(APIView):
	"""
	API endpoint to get a Redditor data by the name. redditors/<str:name>
	GET request returns the redditor data.
	Expects a valid bearer token in the Authorization header.
	"""

	authentication_classes = [MyTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, name, Format=None):
		logger.info('-' * 100)
		logger.info('Get redditor data request...')

		# Gets the reddit instance from the user in request (ClientOrg)
		client_org = request.user
		reddit = Utils.new_client_request(client_org)
		# Get redditor instance with the name provided
		redditor = RedditorsUtils.get_redditor_if_exists(name, reddit)
		if redditor is None:
			raise exceptions.NotFound(
				detail={'detail': f'No redditor exists with the name: {name}.'})

		# Get data I need from subreddit instance
		redditor_data = RedditorsUtils.get_redditor_data(redditor)
		# Enqueue this in a redis queue job later
		RedditorsUtils.create_or_update(redditor_data)

		return Response(redditor_data, status=status.HTTP_200_OK)

