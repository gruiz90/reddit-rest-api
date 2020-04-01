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


class Submission(APIView):
    """
    API endpoint to get/delete a Submission by the id provided.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Submission "{id}" info request =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if not submission:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        # Get data I need from submission instance
        submission_data = SubmissionsUtils.get_submission_data(submission)
        return Response(submission_data, status=status.HTTP_200_OK)

    def delete(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Submission "{id}" delete =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if not submission:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        status_code = status.HTTP_200_OK
        if not reddit.read_only:
            # Only can delete the submission if author is the same as the reddit instance
            # So check for submission redditor and reddit redditor
            submission_redditor = submission.author
            if submission_redditor:
                redditor_id, redditor_name = ClientsUtils.get_redditor_id_name(
                    client_org
                )
                if submission_redditor.id == redditor_id:
                    # Try to delete the submission now
                    try:
                        submission.delete()
                        msg = f'Submission \'{id}\' successfully deleted.'
                        logger.info(msg)
                    except Exception as ex:
                        msg = (
                            f'Error deleting submission. Exception raised: {repr(ex)}.'
                        )
                        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                        logger.error(msg)
                else:
                    msg = (
                        f'Cannot delete the submission with id: {id}. '
                        f'The authenticated reddit user u/{redditor_name} '
                        f'needs to be the same as the submission\'s author u/{submission_redditor.name}'
                    )
                    status_code = status.HTTP_403_FORBIDDEN
                    logger.info(msg)
            else:
                msg = (
                    f'Cannot delete the submission with id: {id}. '
                    'The submission was already deleted or there is no '
                    'way to verify the author at this moment.'
                )
                status_code = status.HTTP_404_NOT_FOUND
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
                        'detail': f'Vote value {vote} outside allowed integer range (-1<=vote<=1).'
                    }
                )
        except ValueError:
            raise exceptions.ParseError(
                detail={'detail': f'The vote value must be an integer: -1 | 0 | 1.'}
            )

        return vote

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Submission "{id}" vote =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if not submission:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        # Get vote value from data json and check if valid
        vote_value = self._validate_vote_value(request.data.get('vote_value'))

        submission_data = None
        status_code = status.HTTP_200_OK
        if reddit.read_only:
            msg = f'Vote action \'dummy\' successful for submission with id: {id}.'
        else:
            try:
                if vote_value == -1:
                    vote_action = 'Downvote'
                    submission.downvote()
                elif vote_value == 0:
                    vote_action = 'Clear Vote'
                    submission.clear_vote()
                else:
                    vote_action = 'Upvote'
                    submission.upvote()
                submission_data = SubmissionsUtils.get_submission_data_simple(
                    submission
                )
                msg = f'Vote action \'{vote_action}\' successful for submission with id: {id}.'
                logger.info(msg)
            except Exception as ex:
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                msg = (
                    f'Error posting vote to submission with id: {id}. '
                    f'Exception raised: {repr(ex)}.'
                )
                logger.error(msg)

        return Response(
            {'detail': msg, 'submission': submission_data}, status=status_code,
        )


class SubmissionCrosspost(APIView):
    """
        API endpoint to crosspost a submission to a target subreddit.\n
        JSON data params:\n
                    subreddit=[string] –- Name of the subreddit or Subreddit object to crosspost into.
                    title=[string] –- Title of the submission. Will use this submission’s title if None (default: None).
                    flair_id=[string] -- The flair template to select (default: None)
                    flair_text=[string] -- If the template’s flair_text_editable value is True, this value will set a custom text (default: None).
                    send_replies=[bool] -- When True, messages will be sent to the submission author when comments are made to the submission (default: True).
                    nsfw=[bool] -- Whether or not the submission should be marked NSFW (default: False).
                    spoiler=[bool] -- Whether or not the submission should be marked as a spoiler (default: False).
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Submission "{id}" crosspost =>')

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
                    'detail': (
                        'A subreddit value corresponding to an existent '
                        'subreddit name must be provided in the json data.'
                    )
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
                msg = (
                    f'New crosspost submission created in r/{subreddit_name} '
                    f'by u/{redditor_name} with id: {crosspost.id}.'
                )
                logger.info(msg)
            except Exception as ex:
                if isinstance(ex, Forbidden):
                    msg = (
                        f'Cannot create the crosspost submission with id: {id}. '
                        f'Forbidden exception: {repr(ex)}'
                    )
                    status_code = status.HTTP_403_FORBIDDEN
                else:
                    msg = (
                        f'Error creating crosspost submission with id: {id}. '
                        f'Exception raised: {repr(ex)}.'
                    )
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = f'Reddit instance is read only. Cannot create crosspost submission with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response(
            {'detail': msg, 'cross_submission': crosspost_data}, status=status_code
        )


class SubmissionComments(APIView):
    """
        API endpoint access submision top level comments -> submissions/:id/comments\n
        GET returns a max of 20 top level comments per request. Uses offset to get the rest in different request.\n
        URL query params:\n
                    sort=[best|top|new|controversial|old|q_a] (default=best)
                    limit=[0<int<21] (default=10)
                    offset=[0<=int] (default=0)
                    flat=True|False (default=False)
        POST allows to create a comment in a submission by the id.\n
        JSON data params:\n
                    body - The Markdown formatted content for a comment.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    _sortings = ['best', 'top', 'new', 'controversial', 'old', 'q_a']

    def _validate_query_params(self, sort, flat, limit, offset):
        if sort not in self._sortings:
            raise exceptions.ParseError(detail={'detail': f'Sort type {sort} invalid.'})
        elif sort == 'q_a':
            sort = 'q&a'

        try:
            flat = bool(flat)
        except ValueError:
            raise exceptions.ParseError(
                detail={'detail': f'flat parameter must be a boolean: true | false.'}
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
        logger.info(f'Submission "{id}" comments =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get submission instance with the id provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if not submission:
            raise exceptions.NotFound(
                detail={'detail': f'No submission exists with the id: {id}.'}
            )

        sort = request.query_params.get('sort', 'best')
        flat = request.query_params.get('flat', False)
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)

        sort, limit, offset = self._validate_query_params(sort, flat, limit, offset)
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

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Submission "{id}" reply =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        submission = SubmissionsUtils.get_sub_if_exists(id, reddit)
        if not submission:
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
                msg = (
                    f'New comment posted by u/{redditor_name} with id \'{comment.id}\' '
                    f'to submission with id: {id}'
                )
                logger.info(msg)
            except Exception as ex:
                if isinstance(ex, Forbidden):
                    msg = (
                        f'Cannot create a comment in submission with id: {id}. '
                        f'Forbidden exception: {repr(ex)}'
                    )
                    status_code = status.HTTP_403_FORBIDDEN
                else:
                    msg = (
                        f'Error creating comment in submission with id: {id}. '
                        f'Exception raised: {repr(ex)}.'
                    )
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = f'Reddit instance is read only. Cannot create comment in submission with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg, 'comment': comment_data}, status=status_code)
