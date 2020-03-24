#!/usr/bin/env python3
from datetime import datetime
from .serializers import RedditorSerializer
from .models import Redditor


class RedditorsUtils(object):
    @staticmethod
    def create_or_update(redditor_data):
        # Create or update redditor object
        redditor_obj = Redditor.objects.get_or_none(id=redditor_data['id'])
        serializer = RedditorSerializer(instance=redditor_obj, data=redditor_data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def get_redditor_if_exists(name, reddit):
        redditor = reddit.redditor(name)
        try:
            redditor._fetch()
        except:
            return None
        return redditor

    @staticmethod
    def get_redditor_data_simple(redditor):
        # I need to try fetch for the redditor data here
        try:
            if redditor:
                redditor._fetch()
                return {
                    'id': redditor.id,
                    'name': redditor.name,
                    'created_utc': datetime.utcfromtimestamp(redditor.created_utc),
                    'icon_img': redditor.icon_img,
                    'comment_karma': redditor.comment_karma,
                    'link_karma': redditor.link_karma,
                }
            else:
                return None
        except:
            return None

    @staticmethod
    def get_redditor_data(redditor):
        return {
            'id': redditor.id,
            'name': redditor.name,
            'created_utc': datetime.utcfromtimestamp(redditor.created_utc),
            'has_verified_email': redditor.has_verified_email,
            'icon_img': redditor.icon_img,
            'comment_karma': redditor.comment_karma,
            'link_karma': redditor.link_karma,
            'num_friends': redditor.num_friends
            if hasattr(redditor, 'num_friends')
            else None,
            'is_employee': redditor.is_employee,
            'is_friend': redditor.is_friend,
            'is_mod': redditor.is_mod,
            'is_gold': redditor.is_gold,
        }

    @staticmethod
    def get_dummy_redditor_data():
        return {
            'id': '4rfkxa54',
            'name': 'sfdctest',
            'created_utc': '2019-10-31T19:22:45Z',
            # 'created_utc': datetime.strptime('2019-10-31 19:22:45', '%Y-%m-%d %H:%M:%S'),
            'has_verified_email': True,
            'icon_img': 'https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png',
            'comment_karma': 0,
            'link_karma': 1,
            'num_friends': 0,
            'is_employee': False,
            'is_friend': False,
            'is_mod': False,
            'is_gold': False,
        }
