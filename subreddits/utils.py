#!/usr/bin/env python3
from .models import Subreddit
from .serializers import SubredditSerializer
from datetime import datetime

class sub_utils(object):

	@staticmethod
	def create_or_update(subreddit_data):
		# Create or update subreddit object for this client
		subreddit_obj = Subreddit.objects.get_or_none(id=subreddit_data['id'])
		serializer = SubredditSerializer(
			instance=subreddit_obj, data=subreddit_data)
		serializer.is_valid(raise_exception=True)
		return serializer.save()

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