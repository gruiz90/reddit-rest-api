#!/usr/bin/env python3
from .models import Subreddit
from .serializers import SubredditSerializer
from clients.utils import ClientsUtils
from datetime import datetime
from rest_framework import status, exceptions


class SubredditsUtils(object):
    @staticmethod
    def create_or_update(subreddit_data):
        # Create or update subreddit object for this client
        subreddit_obj = Subreddit.objects.get_or_none(id=subreddit_data['id'])
        serializer = SubredditSerializer(instance=subreddit_obj, data=subreddit_data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def sub_exists(name, reddit):
        try:
            subreddits = reddit.subreddits.search_by_name(name, exact=True)
        except:
            return False, None
        return True, subreddits

    @staticmethod
    def get_sub_if_exists(name, reddit):
        exists, subreddits = SubredditsUtils.sub_exists(name, reddit)
        if exists:
            for sub in subreddits:
                if name.lower() == sub.display_name.lower():
                    return reddit.subreddit(name)
        return None

    @staticmethod
    def get_sub_if_available(name, reddit):
        subreddit = SubredditsUtils.get_sub_if_exists(name, reddit)
        try:
            # Just check if I have access to the id attribute
            if subreddit and subreddit.id:
                return subreddit
        except:
            pass
        return None

    @staticmethod
    def subscribe_action(reddit, logger, name, client_org, subreddit, subscribe=True):
        status_code, msg = status.HTTP_200_OK, None
        if not reddit.read_only:
            _, redditor_name = ClientsUtils.get_redditor_id_name(client_org)
            try:
                subscribed = subreddit.user_is_subscriber
                if not subscribed and subscribe:
                    subreddit.subscribe()
                elif subscribed and not subscribe:
                    subreddit.unsubscribe()
                else:
                    msg = (
                        f'Reddit user u/{redditor_name} already '
                        f'{"subscribed to" if subscribe else "unsubscribed from"} r/{name}.'
                    )
                    logger.info(msg)
                if not msg:
                    msg = (
                        f'Reddit user u/{redditor_name} succesfully '
                        f'{"subscribed to" if subscribe else "unsubscribed from"} r/{name}.'
                    )
                    logger.info(msg)
            except Exception as ex:
                msg = (
                    f'Error {"subscribing" if subscribe else "unsubscribing"} '
                    f'u/{redditor_name} {"to" if subscribe else "from"} r/{name}. '
                    f'Exception raised: {repr(ex)}.'
                )
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                logger.error(msg)
        else:
            msg = (
                f'Reddit instance is read only. Cannot '
                f'{"subscribe to" if subscribe else "unsubscribe from"} subreddit r/{name}.'
            )
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            logger.warn(msg)
        return status_code, msg

    @staticmethod
    def check_and_get_sub(subreddit_name, reddit):
        if not subreddit_name or not isinstance(subreddit_name, str):
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
        return subreddit

    @staticmethod
    def get_subreddit_data(subreddit):
        return {
            'id': subreddit.id,
            'name': subreddit.name,
            'display_name': subreddit.display_name,
            'description': subreddit.description,
            'description_html': subreddit.description_html,
            'public_description': subreddit.public_description,
            'created_utc': datetime.utcfromtimestamp(subreddit.created_utc),
            'subscribers': subreddit.subscribers,
            'spoilers_enabled': subreddit.spoilers_enabled,
            'over18': subreddit.over18,
            'can_assign_link_flair': subreddit.can_assign_link_flair,
            'can_assign_user_flair': subreddit.can_assign_user_flair,
        }

    @staticmethod
    def get_subreddit_data_simple(subreddit):
        return {
            'id': subreddit.id,
            'name': subreddit.name,
            'display_name': subreddit.display_name,
            'public_description': subreddit.public_description,
            'created_utc': datetime.utcfromtimestamp(subreddit.created_utc),
            'subscribers': subreddit.subscribers,
        }
