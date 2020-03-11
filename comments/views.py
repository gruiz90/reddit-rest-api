#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from api.token_authentication import MyTokenAuthentication
from .utils import CommentsUtils

from api.utils import Utils

logger = Utils.init_logger(__name__)


class CommentView(APIView):
    """
	API endpoint to get the Coment data by the id provided.
	"""

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New comment details request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = Utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        # Here I need to call refresh() for some reason to get the actual replies count
        comment.refresh()
        logger.info(f'Total top replies: {len(comment.replies)}')

        comment_data = CommentsUtils.get_comment_data(comment)

        return Response(comment_data, status=status.HTTP_200_OK)


class CommentVoteView(APIView):
    """
	API endpoint to post a vote for a comment by the id.
	data_json: { "vote_value": -1 | 0 | 1}
	"""

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def __validate_vote_value(self, vote):
        if vote is None:
            raise exceptions.ParseError(
                detail={'detail': f'A vote_value must be provided in the json data.'}
            )
        try:
            vote = int(vote)
            if not vote in [-1, 0, 1]:
                raise exceptions.ParseError(
                    detail={
                        'detail': f'Vote value {vote} outside allowed range (-1<=vote<=1).'
                    }
                )
        except ValueError:
            raise exceptions.ParseError(
                detail={'detail': f'The vote value must be a -1, 0 or 1.'}
            )

        return vote

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New comment vote request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = Utils.new_client_request(client_org)
        # Get subreddit instance with the name provided
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        # Get vote value from data json and check if valid
        vote_value = self.__validate_vote_value(request.data.get('vote_value'))

        if reddit.read_only:
            vote_action = 'dummy'
        else:
            if vote_value == -1:
                vote_action = 'Downvote'
                comment.downvote()
            elif vote_value == 0:
                vote_action = 'Clear Vote'
                comment.clear_vote()
            else:
                vote_action = 'Upvote'
                comment.upvote()

        return Response(
            {
                'detail': f'Vote action \'{vote_action}\' successful for comment with id: {id}!'
            },
            status=status.HTTP_200_OK,
        )


class CommentRepliesView(APIView):
    """
	API endpoint to get a comment top level replies. comments/<str:id>/replies
	It returns a max of 20 top level replies per request. Uses offset to get the rest in different request.
				  limit=[0<int<21] (default=10)
				  offset=[0<=int] (default=0)
				  flat=True|False (default=False)
	"""

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def __validate_query_params(self, flat, limit, offset):
        try:
            flat = bool(flat)
        except ValueError:
            raise exceptions.ParseError(
                detail={
                    'detail': f'flat parameter must be a boolean like \'True\' or \'False\'.'
                }
            )

        try:
            limit = int(limit)
            if not 0 < limit < 21:
                raise exceptions.ParseError(
                    detail={
                        'detail': f'Limit {limit} outside allowed range (0<int<21).'
                    }
                )
        except ValueError:
            raise exceptions.ParseError(
                detail={'detail': f'limit parameter must be an integer.'}
            )
        try:
            offset = int(offset)
            if offset < 0:
                raise exceptions.ParseError(
                    detail={
                        'detail': f'Offset {offset} outside allowed range (offset>=0).'
                    }
                )
        except ValueError:
            raise exceptions.ParseError(
                detail={'detail': f'offset parameter must be an integer.'}
            )

        return limit, offset

    def _get_replies(self, comment, flat):
        comment.replies.replace_more(limit=0)
        if flat:
            return comment.replies.list()
        else:
            return comment.replies

    def get(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New comment get replies request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        client_org = request.user
        reddit = Utils.new_client_request(client_org)
        # Get submission instance with the id provided
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        flat = request.query_params.get('flat', False)
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)

        limit, offset = self.__validate_query_params(flat, limit, offset)
        logger.info(f'Limit: {limit}')
        logger.info(f'Offset: {offset}')

        # Here I need to call refresh() for some reason to get the actual replies count
        comment.refresh()
        logger.info(f'Total top replies: {len(comment.replies)}')

        # Get replies generator from the comment instance
        replies_generator = self._get_replies(comment, flat)

        replies = []
        for index, reply in enumerate(replies_generator, start=1):
            if index > offset:
                replies.append(CommentsUtils.get_comment_data_simple(reply))
                # For some reason the comment_limit attr in the submission instance does not work
                # as suggested in docs, so breaking here when it reaches limit comments
                if len(replies) > limit - 1:
                    break

        logger.info(f'Total comments retrieved: {len(replies)}')

        return Response(
            {
                'replies': replies,
                'limit_request': limit,
                'offset': offset,
                'flat': flat,
            },
            status=status.HTTP_200_OK,
        )

