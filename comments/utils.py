#!/usr/bin/env python3
from datetime import datetime
from prawcore import NotFound
from praw.exceptions import ClientException
from redditors.utils import RedditorsUtils
from subreddits.utils import SubredditsUtils
from submissions.utils import SubmissionsUtils


class CommentsUtils(object):

    # @staticmethod
    # def _exists(id, reddit):
    # 	exists = True
    # 	try:
    # 		reddit.submissions.get_submission(submission_id=id)
    # 	except NotFound:
    # 		exists = False
    # 	return exists

    @staticmethod
    def get_comment_if_exists(id, reddit):
        comment = reddit.comment(id)
        try:
            comment._fetch()
            return comment
        except ClientException:
            return None

    @staticmethod
    def get_comment_data_simple(comment):
        return {
            'id': comment.id,
            'body': comment.body,
            'created_utc': datetime.utcfromtimestamp(comment.created_utc),
            'author_name': comment.author.name if comment.author is not None else None,
            'score': comment.score,
            'subreddit_id': comment.subreddit_id,
            'link_id': comment.link_id,
            'parent_id': comment.parent_id,
            'has_replies': len(comment.replies) > 0,
        }

    @staticmethod
    def get_comment_data(comment):
        return {
            'id': comment.id,
            'body': comment.body,
            'created_utc': datetime.utcfromtimestamp(comment.created_utc),
            'author': RedditorsUtils.get_redditor_data_simple(comment.author),
            'score': comment.score,
            'permalink': comment.permalink,
            'link_id': comment.link_id,
            'parent_id': comment.parent_id,
            'submission': SubmissionsUtils.get_submission_data_simple(
                comment.submission
            ),
            'subreddit': SubredditsUtils.get_subreddit_data_simple(comment.subreddit),
            'has_replies': len(comment.replies) > 0,
            'is_submitter': comment.is_submitter,
            'distinguished': comment.distinguished,
            'edited': comment.edited,
            'stickied': comment.stickied,
        }

