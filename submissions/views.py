#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from api.token_authentication import MyTokenAuthentication
from .utils import SubmissionsUtils
from comments.utils import CommentsUtils

from api.utils import Utils
logger = Utils.init_logger(__name__)


class SubmissionView(APIView):
	"""
	API endpoint to get the Submission data by the id provided.
	"""

	authentication_classes = [MyTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, id, Format=None):
		logger.info('-' * 100)
		logger.info('New submission details request...')

		# Gets the reddit instance from the user in request (ClientOrg)
		client_org = request.user
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
		if submission is None:
			raise exceptions.NotFound(
				detail={'detail': f'No submission exists with the id: {id}.'})

		# Get data I need from subreddit instance
		submission_data = SubmissionsUtils.get_submission_data(submission)

		return Response(submission_data, status=status.HTTP_200_OK)


class SubmissionVoteView(APIView):
	"""
	API endpoint to post a vote for a submission by the id.
	data_json: { "vote_value": -1 | 0 | 1}
	"""

	authentication_classes = [MyTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def __validate_vote_value(self, vote):
		if vote is None:
			raise exceptions.ParseError(
				detail={'detail': f'A vote_value must be provided in the json data.'})
		try:
			vote = int(vote)
			if not vote in [-1, 0, 1]:
				raise exceptions.ParseError(
					detail={'detail': f'Vote value {vote} outside allowed range (-1<=vote<=1).'})
		except ValueError:
			raise exceptions.ParseError(
				detail={'detail': f'The vote value must be a -1, 0 or 1.'})

		return vote

	def post(self, request, id, Format=None):
		logger.info('-' * 100)
		logger.info('New submission vote request...')

		# Gets the reddit instance from the user in request (ClientOrg)
		client_org = request.user
		reddit = Utils.new_client_request(client_org)
		# Get subreddit instance with the name provided
		submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
		if submission is None:
			raise exceptions.NotFound(
				detail={'detail': f'No submission exists with the id: {id}.'})

		# Get vote value from data json and check if valid
		vote_value = self.__validate_vote_value(request.data.get('vote_value'))

		if reddit.read_only:
			vote_action = 'dummy'
		else:
			if vote_value == -1:
				vote_action = 'Downvote'
				submission.downvote()
			elif vote_value == 0:
				vote_action = 'Clear Vote'
				submission.clear_vote()
			else:
				vote_action = 'Upvote'
				submission.upvote()

		return Response({'detail': f'Vote action \'{vote_action}\' successful for submission with id: {id}!'},
						status=status.HTTP_200_OK)


class SubmissionCommentsView(APIView):
	"""
	API endpoint to get a Submission top level comments. submissions/<str:id>/comments
	It returns a max of 20 top level comments per request. Uses offset to get the rest in different request.
	query_params: sort=[best|top|new|controversial|old|q&a] (default=best)
							  limit=[0<int<21] (default=10)
							  offset=[0<=int] (default=0)
							  flat=True|False (default=False)
	"""

	authentication_classes = [MyTokenAuthentication]
	permission_classes = [IsAuthenticated]

	_sortings = ['best', 'top', 'new', 'controversial', 'old', 'q&a']

	def __validate_query_params(self, sort, flat, limit, offset):
		if sort not in self._sortings:
			raise exceptions.ParseError(
				detail={'detail': f'Sort type {sort} invalid.'})

		try:
			flat = bool(flat)
		except ValueError:
			raise exceptions.ParseError(
					detail={'detail': f'flat parameter must be an boolean like \'True\' or \'False\'.'})

		try:
			limit = int(limit)
			if not 0 < limit < 21:
				raise exceptions.ParseError(
					detail={'detail': f'Limit {limit} outside allowed range (0<int<21).'})
		except ValueError:
			raise exceptions.ParseError(
				detail={'detail': f'limit parameter must be an integer.'})
		try:
			offset = int(offset)
			if offset < 0:
				raise exceptions.ParseError(
					detail={'detail': f'Offset {offset} outside allowed range (offset>=0).'})
		except ValueError:
			raise exceptions.ParseError(
				detail={'detail': f'offset parameter must be an integer.'})

		return limit, offset

	def _get_comments(self, submission, sort, limit, flat):
		submission.comment_sort = sort
		submission.comment_limit = limit
		submission.comments.replace_more(limit=None)
		if flat:
			return submission.comments.list()
		else:
			return submission.comments

	def get(self, request, id, Format=None):
		logger.info('-' * 100)
		logger.info('New submission get comments request...')

		# Gets the reddit instance from the user in request (ClientOrg)
		client_org = request.user
		reddit = Utils.new_client_request(client_org)
		# Get submission instance with the id provided
		submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
		if submission is None:
			raise exceptions.NotFound(
				detail={'detail': f'No submission exists with the id: {id}.'})

		sort = request.query_params.get('sort', 'best')
		flat = request.query_params.get('flat', False)
		limit = request.query_params.get('limit', 10)
		offset = request.query_params.get('offset', 0)

		limit, offset = self.__validate_query_params(sort, flat, limit, offset)
		logger.info(f'Sort type: {sort}')
		logger.info(f'Limit: {limit}')
		logger.info(f'Offset: {offset}')
		logger.info(f'Flat: {flat}')

		# Get submissions generator according to query_params and with the limit + offset?
		comments_generator = self._get_comments(
			submission, sort, limit + offset, flat)

		comments = []
		for index, comment in enumerate(comments_generator, start=1):
			if index > offset:
				comments.append(CommentsUtils.get_comment_data_simple(comment))
				# For some reason the comment_limit attr in the submission instance does not work
				# as suggested in docs, so breaking here when it reaches limit comments
				if len(comments) > limit-1:
					break

		logger.info(f'Total comments retrieved: {len(comments)}')

		return Response({'comments': comments, 'sort_type': sort,
						 'limit_request': limit, 'offset': offset, 'flat': flat},
						status=status.HTTP_200_OK)
