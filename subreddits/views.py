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
			logger.info('Client is not subscribed, so I need to subscribe him here..')
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
			subreddits.append(sub_utils.get_subreddit_data(sub))

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


class SubredditSubmissions(APIView):
	"""
	API endpoint to get a Subreddit submissions. subreddits/<str:name>/submissions
	query_params: sort=[controversial|gilded|hot|new|rising|top] (default=hot)
				  time_filter=[all|day|hour|month|week|year] (default=all)
				  limit=[0<int<11] (default=5)
				  offset=[0<=int<11] (default=0)
	time_filter only used when sort=[controversial|top]
	"""

	authentication_classes = [MyTokenAuthentication]
	permission_classes = [IsAuthenticated]

	__sortings = ['controversial', 'gilded', 'hot', 'new', 'rising', 'top']
	__time_filters = ['all', 'hour', 'month', 'week', 'year']

	def __validate_query_params(self, sort, time_filter, limit, offset):
		if sort not in self.__sortings:
			raise exceptions.ParseError(
                detail={'detail': f'Sort type {sort} invalid.'})
		elif sort == 'controversial' or sort == 'top':
			if time_filter not in self.__time_filters:
				raise exceptions.ParseError(
                	detail={'detail': f'Time filter {time_filter} invalid.'})
		try:
			limit = int(limit)
			logger.info(limit)
			if not 0 < limit < 6:
				raise exceptions.ParseError(
					detail={'detail': f'Limit {limit} outside allowed range (0<limit<6).'})
		except ValueError:
			raise exceptions.ParseError(
					detail={'detail': f'limit parameter must be an integer.'})

		try:
			offset = int(offset)
			if not 0 <= offset:
				raise exceptions.ParseError(
					detail={'detail': f'Offset {offset} outside allowed range (0<=offset).'})
		except ValueError:
			raise exceptions.ParseError(
					detail={'detail': f'offset parameter must be an integer.'})

		return limit, offset


	def __get_submissions(self, subreddit, sort, time_filter, limit):
		if sort == 'hot':
			return subreddit.hot(limit=limit)
		elif sort == 'rising':
			return subreddit.rising(limit=limit)
		elif sort == 'new':
			return subreddit.new(limit=limit)
		elif sort == 'gilded':
			return subreddit.gilded(limit=limit)
		elif sort == 'controversial':
			return subreddit.controversial(time_filter=time_filter, limit=limit)
		else:
			return subreddit.top(time_filter=time_filter, limit=limit)


	def get(self, request, name, Format=None):
		logger.info('-' * 100)
		logger.info('New subreddit get submissions request...')

		# Gets the reddit instance from the user in request (ClientOrg)
		client_org = request.user
		reddit = utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = sub_utils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

		sort = request.query_params.get('sort', 'hot')
		time_filter = request.query_params.get('time_filter', 'all')
		limit = request.query_params.get('limit', 5)
		offset = request.query_params.get('offset', 0)

		limit, offset = self.__validate_query_params(sort, time_filter, limit, offset)
		logger.info(f'Sort type: {sort}')
		logger.info(f'Time filter: {time_filter}')
		logger.info(f'limit: {limit}')
		logger.info(f'offset: {offset}')

		# Get submissions generator according to query_params and with the limit + offset?
		submissions_generator = self.__get_submissions(subreddit, sort, time_filter, limit + offset)

		submissions = []
		for index, sub in enumerate(submissions_generator, start=1):
			if index > offset:
				submissions.append(sub_utils.get_submission_data(sub))
		logger.info(f'Total submissions: {len(submissions)}')

		return Response({'submissions': submissions, 'sort': sort,
                   'time_filter': time_filter, 'limit': limit, 'offset': offset},
                  status=status.HTTP_200_OK)
