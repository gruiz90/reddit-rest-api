from django.db import models
from herokuredditapi.modelmanager import MyModelManager
from clients.models import ClientOrg


class Subreddit(models.Model):
	id = models.CharField(max_length=64, primary_key=True,
						  help_text='The ID of the subreddit.')
	name = models.CharField(
		max_length=256, help_text='Fullname of the subreddit.')
	display_name = models.CharField(
		max_length=256, help_text='Name of the subreddit.', db_index=True)
	description = models.TextField(
		null=True, help_text='Subreddit description, in Markdown.')
	description_html = models.TextField(null=True,
										help_text='Subreddit description, in HTML.')
	public_description = models.TextField(null=True,
										  help_text=('Description of the subreddit, '
													 'shown in searches and on the'
													 '"You must be invited to visit this community"'
													 'page(if applicable).')
										  )
	created_utc = models.DateTimeField(
		help_text='Time the subreddit was created, from Unix Time to Datetime format.')
	subscribers = models.PositiveIntegerField(
		'subscribers count', default=0, help_text='Count of subscribers.')
	spoilers_enabled = models.BooleanField(null=True,
										   help_text='Whether the spoiler tag feature is enabled.')
	over18 = models.BooleanField(
		'nsfw', null=True, help_text='Whether the subreddit is NSFW.')
	can_assign_link_flair = models.BooleanField(
		null=True, help_text='Whether users can assign their own link flair.')
	can_assign_user_flair = models.BooleanField(
		null=True, help_text='Whether users can assign their own user flair.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# Clients this subreddit has connections to
	clients = models.ManyToManyField(ClientOrg)

	objects = MyModelManager()

	class Meta:
		ordering = ['name']
		get_latest_by = ['created_at']
		verbose_name_plural = 'Subreddits'

	def __str__(self):
		result = [f'Subreddit\'s Name: {self.name}', f'Created UTC: {self.created_utc}',
				  f'Description: {self.description}', f'Total subs: {self.subscribers}', ]
		return ', '.join((str(x) for x in result))
