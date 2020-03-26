#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .models import Subreddit
from .serializers import SubredditSerializer
from .utils import SubredditsUtils
from submissions.utils import SubmissionsUtils
from clients.utils import ClientsUtils
from api.token_authentication import MyTokenAuthentication
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
        logger.info(f'Subreddit "{name}" connect =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

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
        logger.info(f'Subreddit "{name}" disconnect =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        subreddit_obj = Subreddit.objects.get_or_none(id=subreddit.id)
        if subreddit_obj is None:
            raise exceptions.NotFound(
                detail={
                    'detail': 'No subreddit found with the name provided to make the disconnection.'
                }
            )
        # Remove the client connection from both sides
        subreddit_obj.clients.remove(client_org)
        client_org.subreddit_set.remove(subreddit_obj)

        return Response(
            data={'detail': 'Client disconnected subreddit succesfully.'},
            status=status.HTTP_200_OK,
        )


class SubredditInfo(APIView):
    """
    API endpoint to get the Subreddit data by the name provided.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info(f'Subreddit "{name}" info request =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        # Get data I need from subreddit instance
        subreddit_data = SubredditsUtils.get_subreddit_data(subreddit)
        # Enqueue this in a redis queue job later
        SubredditsUtils.create_or_update(subreddit_data)

        return Response(subreddit_data, status=status.HTTP_200_OK)


class SubredditSubscriptions(APIView):
    """
    API endpoint to get a list of subreddits subscriptions for the client.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        logger.info('-' * 100)
        logger.info(f'Subreddits subscriptions for client =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)

        if reddit.read_only:
            subreddits = []
        else:
            reddit_user = reddit.user
            subreddits = [
                SubredditsUtils.get_subreddit_data_simple(sub)
                for sub in reddit_user.subreddits()
            ]

        return Response({'subscriptions': subreddits}, status=status.HTTP_200_OK)


class SubredditRules(APIView):
    """
    API endpoint to get the rules of a subreddit by name.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info(f'Subreddit "{name}" rules =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        return Response(subreddit.rules(), status=status.HTTP_200_OK)


class SubredditSubscribe(APIView):
    """
    API endpoint to subscribe a Salesforce org client to a subreddit by the name.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info(f'Subreddit "{name}" subscribe =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        status_code = status.HTTP_200_OK
        if not reddit.read_only:
            _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
            if not subreddit.user_is_subscriber:
                try:
                    subreddit.subscribe()
                    msg = f'Reddit user u/{redditor_name} succesfully subscribed to r/{name}.'
                    logger.info(msg)
                except Exception as ex:
                    msg = f'Error subscribing u/{redditor_name} to r/{name}. Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                    logger.error(msg)
            else:
                msg = f'Reddit user u/{redditor_name} already subscribed to r/{name}.'
                logger.info(msg)
        else:
            msg = (
                f'Reddit instance is read only. Cannot subscribe to subreddit r/{name}.'
            )
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg}, status=status_code)


class SubredditUnsubscribe(APIView):
    """
    API endpoint to unsubscribe a Salesforce org client from a subreddit by the name.
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info(f'Subreddit "{name}" unsubscribe =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        status_code = status.HTTP_200_OK
        if not reddit.read_only:
            _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
            if subreddit.user_is_subscriber:
                try:
                    subreddit.unsubscribe()
                    msg = f'Reddit user u/{redditor_name} succesfully unsubscribed from r/{name}.'
                    logger.info(msg)
                except Exception as ex:
                    msg = f'Error unsubscribing u/{redditor_name} from r/{name}. Exception raised: {repr(ex)}.'
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                    logger.error(msg)
            else:
                msg = (
                    f'Reddit user u/{redditor_name} already unsubscribed from r/{name}.'
                )
                logger.info(msg)
        else:
            msg = f'Reddit instance is read only. Cannot unsubscribe from subreddit r/{name}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response({'detail': msg}, status=status_code)


class SubredditSubmissions(APIView):
    """
    API endpoint to get a Subreddit submissions. subreddits/<str:name>/submissions
    It returns a max of 5 submissions per request. Uses offset to get the rest in different request.
    query_params: sort=[controversial|gilded|hot|new|rising|top] (default=hot)
                  time_filter=[all|day|hour|month|week|year] (default=all)
                  offset=[0<=int<11] (default=0)
    time_filter only used when sort=[controversial|top]
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    _sortings = ['controversial', 'gilded', 'hot', 'new', 'rising', 'top']
    _time_filters = ['all', 'day', 'hour', 'month', 'week', 'year']

    def _validate_query_params(self, sort, time_filter, offset):
        if sort not in self._sortings:
            raise exceptions.ParseError(detail={'detail': f'Sort type {sort} invalid.'})
        elif sort == 'controversial' or sort == 'top':
            if time_filter not in self._time_filters:
                raise exceptions.ParseError(
                    detail={'detail': f'Time filter {time_filter} invalid.'}
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
        logger.info(f'Subreddit "{name}" submissions =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, _ = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        sort = request.query_params.get('sort', 'hot')
        time_filter = request.query_params.get('time_filter', 'all')
        offset = request.query_params.get('offset', 0)

        offset = self._validate_query_params(sort, time_filter, offset)
        logger.info(f'Sort type: {sort}')
        logger.info(f'Time filter: {time_filter}')
        logger.info(f'offset: {offset}')

        # Get submissions generator according to query_params and with the limit + offset?
        submissions_generator = self._get_submissions(
            subreddit, sort, time_filter, offset + 5
        )

        submissions = [
            SubmissionsUtils.get_submission_data_simple(sub)
            for index, sub in enumerate(submissions_generator, start=1)
            if index > offset
        ]
        logger.info(f'Total submissions: {len(submissions)}')

        return Response(
            {
                'submissions': submissions,
                'sort_type': sort,
                'time_filter': time_filter,
                'offset': offset,
            },
            status=status.HTTP_200_OK,
        )


class SubredditSubmitSubmission(APIView):
    """
    API endpoint to submit a text, link, image or video submission to a subreddit
    """

    authentication_classes = [MyTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, name, Format=None):
        logger.info('-' * 100)
        logger.info(f'Subreddit "{name}" post submission =>')

        # Gets the reddit instance from the user in request (ClientOrg)
        reddit, client_org = Utils.new_client_request(request.user)
        # Get subreddit instance with the name provided
        subreddit = SubredditsUtils.get_sub_if_available(name, reddit)
        if subreddit is None:
            raise exceptions.NotFound(
                detail={'detail': f'No subreddit exists with the name: {name}.'}
            )

        # Get required data values
        title = request.data.get('title')
        if title is None:
            raise exceptions.ParseError(
                detail={'detail': f'A title must be provided in the json data.'}
            )
        selftext = request.data.get('selftext')
        url = request.data.get('url')

        if not selftext and not url:
            # Then it can be an image or video/gif post
            image_path = request.data.get('image_path')
            if not image_path:
                video_path = request.data.get('video_path')
                if video_path:
                    videogif = request.data.get('videogif', False)
                    thumbnail_path = request.data.get('thumbnail_path')
                else:
                    raise exceptions.ParseError(
                        detail={
                            'detail': (
                                'Either a selftext, url, image_path or video_path '
                                'must be provided in the json data.'
                            )
                        }
                    )

        # Now get optional data values
        flair_id = request.data.get('flair_id')
        flair_text = request.data.get('flair_text')
        resubmit = request.data.get('resubmit', True)
        send_replies = request.data.get('send_replies', True)
        nsfw = request.data.get('nsfw', False)
        spoiler = request.data.get('spoiler', False)
        collection_id = request.data.get('collection_id', False)

        status_code = status.HTTP_201_CREATED
        submission_data = None
        if not reddit.read_only:
            try:
                submission = None
                if selftext or url:
                    submission = subreddit.submit(
                        title,
                        selftext,
                        url,
                        flair_id,
                        flair_text,
                        resubmit,
                        send_replies,
                        nsfw,
                        spoiler,
                        collection_id,
                    )
                elif image_path:
                    # Not waiting the response here.. Not using websockets
                    subreddit.submit_image(
                        title,
                        image_path,
                        flair_id,
                        flair_text,
                        resubmit,
                        send_replies,
                        nsfw,
                        spoiler,
                        collection_id=collection_id,
                        without_websockets=True,
                    )
                else:
                    # Not waiting the response here.. Not using websockets
                    subreddit.submit_video(
                        title,
                        video_path,
                        videogif,
                        thumbnail_path,
                        flair_id,
                        flair_text,
                        resubmit,
                        send_replies,
                        nsfw,
                        spoiler,
                        collection_id=collection_id,
                        without_websockets=True,
                    )
                _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
                if submission:
                    msg = f'New text/link submission created in r/{name} by u/{redditor_name} with id: {submission.id}.'
                    submission_data = SubmissionsUtils.get_submission_data(submission)
                else:
                    msg = f'New image/video/gif submission created in r/{name} by u/{redditor_name}.'
                logger.info(msg)
            except Exception as ex:
                msg = f'Error creating submission. Exception raised: {repr(ex)}.'
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = f'Reddit instance is read only. Cannot submit a post creation in r/{name}.'
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)

        return Response(
            {'detail': msg, 'submission': submission_data}, status=status_code
        )
