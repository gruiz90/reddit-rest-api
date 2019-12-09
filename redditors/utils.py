#!/usr/bin/env python3
from datetime import datetime
from .serializers import RedditorSerializer
from .models import Redditor
from prawcore import NotFound


class RedditorsUtils(object):

	@staticmethod
	def create_or_update(redditor_data):
		# Create or update redditor object
		redditor_obj = Redditor.objects.get_or_none(id=redditor_data['id'])
		serializer = RedditorSerializer(
			instance=redditor_obj, data=redditor_data)
		serializer.is_valid(raise_exception=True)
		return serializer.save()

	@staticmethod
	def redditor_exists(name, reddit):
		exists = True
		try:
			reddit.redditors.search_by_name(name, exact=True)
		except NotFound:
			exists = False
		return exists

	@staticmethod
	def get_redditor_if_exists(name, reddit):
		redditor = reddit.redditor(name)
		try:
			redditor._fetch()
			return redditor
		except NotFound:
			return None

	@staticmethod
	def get_redditor_data_simple(redditor):
		return {
			'id': redditor.id,
			'name': redditor.name,
			'created_utc': datetime.utcfromtimestamp(redditor.created_utc),
			'icon_img': redditor.icon_img,
			'comment_karma': redditor.comment_karma,
			'link_karma': redditor.link_karma,
		}

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
			'num_friends': redditor.num_friends if hasattr(redditor, 'num_friends') else None,
			'is_employee': redditor.is_employee,
			'is_friend': redditor.is_friend,
			'is_mod': redditor.is_mod,
			'is_gold': redditor.is_gold,
		}
