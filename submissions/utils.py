#!/usr/bin/env python3
from datetime import datetime
from prawcore import NotFound
from redditors.utils import RedditorsUtils


class SubmissionsUtils(object):

	@staticmethod
	def sub_exists(id, reddit):
		exists = True
		try:
			reddit.submissions.get_submission(submission_id=id)
		except NotFound:
			exists = False
		return exists

	@staticmethod
	def get_sub_if_exists(id, reddit):
		sub = reddit.submission(id=id)
		try:
			sub._fetch()
			return sub
		except NotFound:
			return None

	@staticmethod
	def get_submission_data_simple(submission):
		return {
			'id': submission.id,
			'name': submission.name,
			'title': submission.title,
			'created_utc': datetime.utcfromtimestamp(submission.created_utc),
			'author_name': submission.author.name,
			'num_comments': submission.num_comments,
			'score': submission.score,
			'url': submission.url,
		}

	@staticmethod
	def get_submission_data(submission):
		return {
			'id': submission.id,
			'name': submission.name,
			'title': submission.title,
			'created_utc': datetime.utcfromtimestamp(submission.created_utc),
			'author': RedditorsUtils.get_redditor_data_simple(submission.author),
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

