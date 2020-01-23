from django.db import models
from herokuredditapi.modelmanager import MyModelManager


class Redditor(models.Model):
	id = models.CharField(max_length=64, primary_key=True,
                       help_text='The ID of the Redditor.')
	name = models.CharField(
		max_length=256, help_text='The Redditor’s username.', db_index=True)
	created_utc = models.DateTimeField(
		help_text='Time the account was created, from Unix Time to Datetime format.')
	has_verified_email = models.BooleanField(
		default=False, help_text='Whether or not the Redditor has verified their email.')
	icon_img = models.URLField(help_text='The url of the Redditors’ avatar.')
	comment_karma = models.IntegerField(
		default=0, help_text='The comment karma for the Redditor.')
	link_karma = models.IntegerField(
		default=0, help_text='The link karma for the Redditor.')
	num_friends = models.PositiveIntegerField(
		'friends count', null=True, default=0, help_text='Count of friends.')
	is_employee = models.BooleanField(null=True,
                                   help_text='Whether or not the Redditor is a Reddit employee.')
	is_friend = models.BooleanField(
		null=True, help_text='Whether or not the Redditor is friends with the authenticated user.')
	is_mod = models.BooleanField(
		null=True, help_text='Whether or not the Redditor mods any subreddits.')
	is_gold = models.BooleanField(
		null=True, help_text='Whether or not the Redditor has active gold status.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = MyModelManager()

	class Meta:
		ordering = ['name']
		get_latest_by = ['created_at']
		verbose_name_plural = "Redditors"

	def __str__(self):
		result = [f'Redditor\'s Name: {self.name}', f'Created UTC: {self.created_utc}',
                    f'Comment Karma: {self.comment_karma}', f'Link Karma: {self.link_karma}', ]
		return ', '.join((str(x) for x in result))
