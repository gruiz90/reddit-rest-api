#!/usr/bin/env python3
from .models import Subreddit
from .serializers import SubredditSerializer
from datetime import datetime
from prawcore import NotFound


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
	def sub_exists(name, reddit):
		exists = True
		try:
			reddit.subreddits.search_by_name(name, exact=True)
		except NotFound:
			exists = False
		return exists

	@staticmethod
	def get_sub_if_exists(name, reddit):
		if sub_utils.sub_exists(name, reddit):
			return reddit.subreddit(name)
		return None

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

	@staticmethod
	def get_submission_data(submission):
		return {
			'id': submission.id,
			'name': submission.name,
			'title': submission.title,
			'created_utc': datetime.utcfromtimestamp(submission.created_utc),
			'author_name': submission.author.name,
			'num_comments': submission.num_comments,
			'score': submission.score,
			'upvote_ratio': submission.upvote_ratio,
			'permalink': submission.permalink,
			'url': submission.url,
			'is_original_content': submission.is_original_content,
			'is_self': submission.is_self,
			'selftext': submission.selftext,
			'clicked': submission.clicked,
			'distinguished': submission.distinguished,
			'edited': submission.edited,
			'locked': submission.locked,
			'stickied': submission.stickied,
			'spoiler': submission.spoiler,
			'over_18': submission.over_18,
		}

