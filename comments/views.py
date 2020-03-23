#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from prawcore.exceptions import Forbidden

from .utils import CommentsUtils
from clients.utils import ClientsUtils
from api.token_authentication import MyTokenAuthentication
from api.utils import Utils

logger = Utils.init_logger(__name__)


class CommentInfo(APIView):
    """
    API endpoint to get/update/delete a reddit comment by the id provided
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Comment "{id}" info request =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        # Here I need to call refresh() to get the actual replies count
        comment.refresh()
        logger.info(f'Total top replies: {len(comment.replies)}')

        comment_data = CommentsUtils.get_comment_data(comment)
        return Response(comment_data, status=status.HTTP_200_OK)

    def patch(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Comment "{id}" patch =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        # Get the markdown content from json body attribute
        markdown_body = Utils.validate_body_value(request.data.get('body'))

        status_code = status.HTTP_200_OK
        updated_comment_data = None
        if not reddit.read_only:
            # Only can modify the comment if author is the same as the client redditor
            # So check for comment redditor and client data
            comment_redditor = comment.author
            redditor_id, redditor_name = ClientsUtils.get_redditor_id_name(client_org)

            if comment_redditor.id == redditor_id:
                # Try to delete the comment now
                try:
                    updated_comment = comment.edit(markdown_body)
                    updated_comment_data = CommentsUtils.get_comment_data(
                        updated_comment
                    )
                    msg = f'Comment "{updated_comment.id}" successfully edited.'
                    logger.info(msg)
                except Exception as ex:
                    msg = f'Error edit comment. Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                    logger.error(msg)
            else:
                msg = f'Cannot edit the comment "{id}". \
                    The authenticated reddit user {redditor_name} \
                        needs to be the same as the comment\'s author: {comment_redditor.name}'
                status_code = status.HTTP_403_FORBIDDEN
                logger.info(msg)
        else:
            msg = f'Reddit instance is read only. Cannot edit comment with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response(
            {'detail': msg, 'comment': updated_comment_data}, status=status_code
        )

    def delete(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Comment "{id}" delete =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        status_code = status.HTTP_200_OK
        if not reddit.read_only:
            # Only can delete the comment if author is the same as the client redditor
            # So check for comment redditor and client data
            comment_redditor = comment.author
            redditor_id, redditor_name = ClientsUtils.get_redditor_id_name(client_org)

            if comment_redditor.id == redditor_id:
                # Try to delete the comment now
                try:
                    comment.delete()
                    msg = f'Comment "{id}" successfully deleted.'
                    logger.info(msg)
                except Exception as ex:
                    msg = f'Error deleting comment. Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                    logger.error(msg)
            else:
                msg = f'Cannot delete the comment "{id}". \
                    The authenticated reddit user {redditor_name} \
                        needs to be the same as the comment\'s author: {comment_redditor.name}'
                status_code = status.HTTP_403_FORBIDDEN
                logger.info(msg)
        else:
            msg = f'Reddit instance is read only. Cannot delete comment with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg}, status=status_code)


class CommentVote(APIView):
    """
    API endpoint to post a vote for a comment by the id.
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
        logger.info(f'Comment "{id}" vote =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        # Get vote value from data json and check if valid
        vote_value = self._validate_vote_value(request.data.get('vote_value'))

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


class CommentReply(APIView):
    """
    API endpoint that post a reply to a comment by the id
    Data in json: body - The Markdown formatted content for a comment.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id, Format=None):
        logger.info('-' * 100)
        logger.info(f'Comment "{id}" reply =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        # Get the markdown content from json body attribute
        markdown_body = Utils.validate_body_value(request.data.get('body'))

        status_code = status.HTTP_201_CREATED
        reply_comment_data = None
        if not reddit.read_only:
            # Try to post the comment to the submission
            try:
                reply_comment = comment.reply(markdown_body)
                reply_comment_data = CommentsUtils.get_comment_data(reply_comment)
                _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
                msg = f'New reply posted by u/{redditor_name} with id "{reply_comment.id}" to comment "{id}"'
                logger.info(msg)
            except Exception as ex:
                if isinstance(ex, Forbidden):
                    msg = f'Cannot create a reply to comment "{id}". Forbidden exception: {repr(ex)}'
                    status_code = status.HTTP_403_FORBIDDEN
                else:
                    msg = f'Error creating reply to comment "{id}". Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = f'Reddit instance is read only. Cannot create reply to comment with id: {id}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response(
            {'detail': msg, 'comment': reply_comment_data}, status=status_code
        )


class CommentReplies(APIView):
    """
    API endpoint to get a comment top level replies. comments/<str:id>/replies
    It returns a max of 20 top level replies per request. Uses offset to get the rest in different request.
                  limit=[0<int<21] (default=10)
                  offset=[0<=int] (default=0)
                  flat=True|False (default=False)
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def _validate_query_params(self, flat, limit, offset):
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
        logger.info(f'Comment "{id}" replies =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get submission instance with the id provided
        comment = CommentsUtils.get_comment_if_exists(id, reddit)
        if comment is None:
            raise exceptions.NotFound(
                detail={'detail': f'No comment exists with the id: {id}.'}
            )

        flat = request.query_params.get('flat', False)
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)

        limit, offset = self._validate_query_params(flat, limit, offset)
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
