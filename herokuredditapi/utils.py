#!/usr/bin/env python3
from rest_framework.views import exception_handler
from django.core.cache import cache
from datetime import datetime

import random
import logging
import colorlog
import os
import praw
import urllib

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


class Utils(object):
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
				redirect_uri=f'{os.environ.get("DOMAIN_URL")}/clients/oauth_callback',
			)

	@staticmethod
	def new_client_request(client_org):
		"""
		Receives the client_org from request.user and returns the authorized reddit instance
		ready to use.
		Arguments:
			client_org {[ClientOrg]} -- [ClientOrg object with validated reddit_token]
		"""
		# If the request is authenticated correctly by the bearer token then I can get
		# the client_org from the request.user. Return tuple from TokenAuthentication:
		# (request.user, request.auth) = (client_org, bearer_token)
		client_org.new_client_request()
		return Utils.get_reddit_instance(token=client_org.reddit_token)


	@staticmethod
	def save_valid_state_in_cache(key, org_id=None):
		state = str(random.randint(0, 65536))
		while cache.has_key(f'{key}_{state}'):
			state = str(random.randint(0, 65536))
		state_data = {'status': 'pending'}
		if org_id:
			state_data['org_id'] = org_id
		cache.set(f'{key}_{state}', state_data, 900)
		return state

	@staticmethod
	def make_url_with_params(path_url, **kwargs):
		return f'{path_url}?{urllib.parse.urlencode(kwargs)}'
