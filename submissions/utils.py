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
			# Check if id exists
			sub.title
			return sub
		except:
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

	@staticmethod
	def get_dummy_submission_data():
		return {
			'id': '78uvdw',
			'name': 't3_78uvdw',
			'title': 'I wrote a Reddit bot in Python',
			'created_utc': '2017-10-26T11:16:44',
			'author': {
				'id': '15xicu',
				'name': 'kindw',
				'created_utc': '2017-03-05T10:43:27',
				'icon_img': 'https://www.redditstatic.com/avatars/avatar_default_15_C18D42.png',
				'comment_karma': 13344,
				'link_karma': 18314
			},
			'num_comments': 53,
			'score': 1173,
			'upvote_ratio': 0.95,
			'permalink': '/r/Python/comments/78uvdw/i_wrote_a_reddit_bot_in_python_a_few_weeks_back/',
			'url': 'https://www.reddit.com/r/Python/comments/78uvdw/i_wrote_a_reddit_bot_in_python_a_few_weeks_back/',
			'is_original_content': False,
			'is_self': True,
			'selftext': 'dummy',
			'clicked': False,
			'distinguished': None,
			'edited': 1527982714.0,
			'locked': False,
			'stickied': False,
			'spoiler': False,
			'over_18': False,
		}

