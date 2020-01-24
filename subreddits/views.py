#!/usr/bin/env python3
from .models import Subreddit
from .serializers import SubredditSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from api.token_authentication import MyTokenAuthentication
from .utils import SubredditsUtils
from submissions.utils import SubmissionsUtils

from api.utils import Utils
logger = Utils.init_logger(__name__)


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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

		logger.info(f'Connecting to Subreddit {subreddit.name}')
		if not reddit.read_only and not subreddit.user_is_subscriber:
			logger.info('Client is not subscribed, so I need to subscribe him here..')
			subreddit.subscribe()
		logger.info(f'Client subscribed: {subreddit.user_is_subscriber}')

		# Get data I need from subreddit instance
		subreddit_data = SubredditsUtils.get_subreddit_data(subreddit)

		# Here for now I'll just save the subreddit_data in a Subreddit Model object
		# But I need to enqueue this into a redis queue, send the data to user as fast as possible
		subreddit_obj = SubredditsUtils.create_or_update(subreddit_data)
		# Add the client_org connection to the object
		subreddit_obj.clients.add(client_org)

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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

		# Get data I need from subreddit instance
		subreddit_data = SubredditsUtils.get_subreddit_data(subreddit)
		# Enqueue this in a redis queue job later
		SubredditsUtils.create_or_update(subreddit_data)

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
		reddit = Utils.new_client_request(client_org)

		if reddit.read_only:
			subreddits = []
		else:
			reddit_user = reddit.user
			subreddits = [SubredditsUtils.get_subreddit_data_simple(sub) 
                            for sub in reddit_user.subreddits()]

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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

		if not reddit.read_only and not subreddit.user_is_subscriber:
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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

		if not reddit.read_only and subreddit.user_is_subscriber:
			subreddit.unsubscribe()
		logger.info(f'Client subscribed: {subreddit.user_is_subscriber}')

		return Response({'detail': f'Client succesfully unsubscribed from {name}.'}, status=status.HTTP_200_OK)


class SubredditSubmissions(APIView):
	"""
	API endpoint to get a Subreddit submissions. subreddits/<str:name>/submissions
	It returns a max of 5 submissions per request. Uses offset to get the rest in different request.
	query_params: sort=[controversial|gilded|hot|new|rising|top] (default=hot)
				  time_filter=[all|day|hour|month|week|year] (default=all)
				  offset=[0<=int<11] (default=0)
	time_filter only used when sort=[controversial|top]
	"""

	authentication_classes = [MyTokenAuthentication]
	permission_classes = [IsAuthenticated]

	_sortings = ['controversial', 'gilded', 'hot', 'new', 'rising', 'top']
	_time_filters = ['all', 'hour', 'month', 'week', 'year']

	def __validate_query_params(self, sort, time_filter, offset):
		if sort not in self._sortings:
			raise exceptions.ParseError(
                            detail={'detail': f'Sort type {sort} invalid.'})
		elif sort == 'controversial' or sort == 'top':
			if time_filter not in self._time_filters:
				raise exceptions.ParseError(
                                    detail={'detail': f'Time filter {time_filter} invalid.'})
		try:
			offset = int(offset)
			if offset < 0:
				raise exceptions.ParseError(
					detail={'detail': f'Offset {offset} outside allowed range (offset>=0).'})
		except ValueError:
			raise exceptions.ParseError(
                            detail={'detail': f'offset parameter must be an integer.'})

		return offset

	def _get_submissions(self, subreddit, sort, time_filter, limit):
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
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
		if subreddit is None:
			raise exceptions.NotFound(
				detail={'detail': f'No subreddit exists with the name: {name}.'})

		sort = request.query_params.get('sort', 'hot')
		time_filter = request.query_params.get('time_filter', 'all')
		offset = request.query_params.get('offset', 0)

		offset = self.__validate_query_params(sort, time_filter, offset)
		logger.info(f'Sort type: {sort}')
		logger.info(f'Time filter: {time_filter}')
		logger.info(f'offset: {offset}')

		# Get submissions generator according to query_params and with the limit + offset?
		submissions_generator = self._get_submissions(
			subreddit, sort, time_filter, offset + 5)

		submissions = [
			SubmissionsUtils.get_submission_data_simple(sub) 
			for index, sub in enumerate(submissions_generator, start=1) if index > offset
		]
		logger.info(f'Total submissions: {len(submissions)}')

		return Response({'submissions': submissions, 'sort_type': sort,
                   'time_filter': time_filter, 'offset': offset},
                  status=status.HTTP_200_OK)
