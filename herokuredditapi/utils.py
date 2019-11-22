from rest_framework.views import exception_handler
import logging
import colorlog
import os
import praw
from .renderers import CustomJSONRenderer
from datetime import datetime
from django.db import models


def custom_json_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        data = {'error': {'code': response.status_code}}
        errors = []
        for field, value in response.data.items():
            errors.append(f'{field}: {value}')
        data['error']['messages'] = errors
        response.data = data
    return response


TESTING_MODE = os.environ.get('LOGLEVEL_DEBUG', False)


class utils(object):
    @staticmethod
    def init_logger(dunder_name) -> logging.Logger:
        log_format = (
            '%(asctime)s - '
            '%(name)s - '
            '%(lineno)d - '
            '%(funcName)s - '
            '%(levelname)s - '
            '%(message)s'
        )
        bold_seq = '\033[1m'
        colorlog_format = (
            f'{bold_seq} '
            '%(log_color)s '
            f'{log_format}'
        )
        colorlog.basicConfig(format=colorlog_format)
        logger = logging.getLogger(dunder_name)

        if TESTING_MODE:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        return logger

    @staticmethod
    def get_reddit_instance(token=None):
        if token:
            return praw.Reddit(
                client_id=os.environ.get('REDDIT_CLIENT_ID'),
                client_secret=os.environ.get(
                    'REDDIT_CLIENT_SECRET'),
                user_agent=os.environ.get('REDDIT_USER_AGENT'),
                refresh_token=token,
            )
        else:
            return praw.Reddit(
                client_id=os.environ.get('REDDIT_CLIENT_ID'),
                client_secret=os.environ.get(
                    'REDDIT_CLIENT_SECRET'),
                user_agent=os.environ.get('REDDIT_USER_AGENT'),
                redirect_uri='http://localhost:8000/accounts/oauth_callback',
            )

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
            'is_employee': redditor.is_employee,
            'is_friend': redditor.is_friend,
            'is_mod': redditor.is_mod,
            'is_gold': redditor.is_gold,
        }
