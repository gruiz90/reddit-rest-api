#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from prawcore.exceptions import Forbidden

from api.token_authentication import MyTokenAuthentication
from .utils import SubmissionsUtils
from comments.utils import CommentsUtils
from clients.utils import ClientsUtils
from subreddits.utils import SubredditsUtils
from api.utils import Utils

logger = Utils.init_logger(__name__)


class SubmissionInfo(APIView):
    """
    API endpoint to get/delete a Submission by the id provided.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New submission details request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if submission is None:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        # Get data I need from submission instance
        submission_data = SubmissionsUtils.get_submission_data(submission)
        return Response(submission_data, status=status.HTTP_200_OK)

    def delete(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New submission delete request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if submission is None:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        status_code = status.HTTP_200_OK
        if not reddit.read_only:
            # Only can delete the submission if author is the same as the reddit instance
            # So check for submission redditor and reddit redditor
            submission_redditor = submission.author
            redditor_id, redditor_name = ClientsUtils.get_redditor_id_name(client_org)

            if submission_redditor.id == redditor_id:
                # Try to delete the submission now
                try:
                    submission.delete()
                    msg = f'Submission "{id}" successfully deleted.'
                    logger.info(msg)
                except Exception as ex:
                    msg = f'Error deleting submission. Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                    logger.error(msg)
            else:
                msg = f'Cannot delete the submission "{id}". \
                    The authenticated reddit user {redditor_name} \
                        needs to be the same as the submission\'s author: {submission_redditor.name}'
                status_code = status.HTTP_403_FORBIDDEN
                logger.info(msg)
        else:
            msg = (
                f'Reddit instance is read only. Cannot delete submission with id: {id}.'
            )
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg}, status=status_code)


class SubmissionVote(APIView):
    """
    API endpoint to post a vote for a submission by the id.
    data_json: { "vote_value": -1 | 0 | 1}
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def _validate_vote_value(self, vote):
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
        logger.info('New submission vote request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if submission is None:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        # Get vote value from data json and check if valid
        vote_value = self._validate_vote_value(request.data.get('vote_value'))

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

        return Response(
            {
                'detail': f'Vote action \'{vote_action}\' successful for submission with id: {id}!'
            },
            status=status.HTTP_200_OK,
        )


class SubmissionReply(APIView):
    """
    API endpoint to post a comment in a submission by the id
    Data in json: body - The Markdown formatted content for a comment.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New submission reply request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if submission is None:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        # Get the markdown content from json body attribute
        markdown_body = Utils.validate_body_value(request.data.get('body'))

        comment_data = None
        status_code = status.HTTP_201_CREATED
        if not reddit.read_only:
            # Try to post the comment to the submission
            try:
                comment = submission.reply(markdown_body)
                comment_data = CommentsUtils.get_comment_data(comment)
                _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
                msg = f'New comment posted by u/{redditor_name} with id "{comment.id}" to submission "{id}"'
                logger.info(msg)
            except Exception as ex:
                if isinstance(ex, Forbidden):
                    msg = f'Cannot create a comment in submission "{id}". Forbidden exception: {repr(ex)}'
                    status_code = status.HTTP_403_FORBIDDEN
                else:
                    msg = f'Error creating comment in submission "{id}". Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = f'Reddit instance is read only. Cannot create comment in submission with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg, 'comment': comment_data}, status=status_code)


class SubmissionCrosspost(APIView):
    """
    API endpoint to crosspost a submission to a target subreddit.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New submission reply request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if not submission:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        # Get required data values from json, in this case only the subreddit name
        # to crosspost the submission
        subreddit_name = request.data.get('subreddit')
        if not subreddit_name:
            raise exceptions.ParseError(
                detail={
                    'detail': 'A subreddit value corresponding to an existent subreddit name must be provided in the json data.'
                }
            )
        else:
            # Check if this subreddit exists?
            subreddit = SubredditsUtils.get_sub_if_available(subreddit_name, reddit)
            if not subreddit:
                raise exceptions.NotFound(
                    detail={
                        'detail': f'No subreddit exists with the name: {subreddit_name}.'
                    }
                )

        # Now get the optional data values
        title = request.data.get('title', None)
        flair_id = request.data.get('flair_id', None)
        flair_text = request.data.get('flair_text', None)
        send_replies = request.data.get('send_replies', True)
        nsfw = request.data.get('nsfw', False)
        spoiler = request.data.get('spoiler', False)

        status_code = status.HTTP_201_CREATED
        crosspost_data = None
        if not reddit.read_only:
            # Try to do the crosspost submission now
            try:
                crosspost = submission.crosspost(
                    subreddit, title, send_replies, flair_id, flair_text, nsfw, spoiler
                )
                crosspost_data = SubmissionsUtils.get_submission_data(crosspost)
                _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
                msg = f'New crosspost submission created in r/{subreddit_name} by u/{redditor_name} with id: {crosspost.id}.'
                logger.info(msg)
            except Exception as ex:
                if isinstance(ex, Forbidden):
                    msg = f'Cannot create the crosspost submission "{id}". Forbidden exception: {repr(ex)}'
                    status_code = status.HTTP_403_FORBIDDEN
                else:
                    msg = f'Error creating crosspost submission "{id}". Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = f'Reddit instance is read only. Cannot create crosspost submission with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg, 'submission': crosspost_data}, status=status_code)


class SubmissionComments(APIView):
    """
    API endpoint to get a Submission top level comments. submissions/<str:id>/comments
    It returns a max of 20 top level comments per request. Uses offset to get the rest in different request.
    query_params: sort=[best|top|new|controversial|old|q_a] (default=best)
                              limit=[0<int<21] (default=10)
                              offset=[0<=int] (default=0)
                              flat=True|False (default=False)
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    _sortings = ['best', 'top', 'new', 'controversial', 'old', 'q_a']

    def __validate_query_params(self, sort, flat, limit, offset):
        if sort not in self._sortings:
            raise exceptions.ParseError(detail={'detail': f'Sort type {sort} invalid.'})
        elif sort == 'q_a':
            sort = 'q&a'

        try:
            flat = bool(flat)
        except ValueError:
            raise exceptions.ParseError(
                detail={
                    'detail': f'flat parameter must be an boolean like \'True\' or \'False\'.'
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

        return sort, limit, offset

    def _get_comments(self, submission, sort, limit, flat):
        submission.comment_sort = sort
        submission.comment_limit = limit
        submission.comments.replace_more(limit=0)
        if flat:
            return submission.comments.list()
        else:
            return submission.comments

    def get(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info('New submission get comments request...')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get submission instance with the id provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if submission is None:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        sort = request.query_params.get('sort', 'best')
        flat = request.query_params.get('flat', False)
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)

        sort, limit, offset = self.__validate_query_params(sort, flat, limit, offset)
        logger.info(f'Sort type: {sort}')
        logger.info(f'Limit: {limit}')
        logger.info(f'Offset: {offset}')
        logger.info(f'Flat: {flat}')

        # Get submissions generator according to query_params and with the limit + offset?
        comments_generator = self._get_comments(submission, sort, limit + offset, flat)

        comments = []
        for index, comment in enumerate(comments_generator, start=1):
            if index > offset:
                comments.append(CommentsUtils.get_comment_data_simple(comment))
                # For some reason the comment_limit attr in the submission instance does not work
                # as suggested in docs, so breaking here when it reaches limit comments
                if len(comments) > limit - 1:
                    break

        logger.info(f'Total comments retrieved: {len(comments)}')

        return Response(
            {
                'comments': comments,
                'sort_type': sort,
                'limit_request': limit,
                'offset': offset,
                'flat': flat,
            },
            status=status.HTTP_200_OK,
        )

