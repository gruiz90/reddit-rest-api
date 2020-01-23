from django.db import models
from django.utils.timezone import now
from encrypted_model_fields.fields import EncryptedCharField
from herokuredditapi.modelmanager import MyModelManager
from redditors.models import Redditor

from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
import binascii


class SalesforceOrg(models.Model):
	org_id = models.CharField(primary_key=True, max_length=64)
	org_name = models.CharField(max_length=256)
	instance_url = models.URLField(max_length=512, blank=True)
	access_token = EncryptedCharField(
		max_length=256, null=True, help_text='Salesforce connected app oauth access token.')
	refresh_token = EncryptedCharField(
		max_length=256, null=True, help_text='Salesforce connected app refresh access token.')
	package_version = models.CharField(max_length=8, blank=True, default='1.0')
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = MyModelManager()

	class Meta:
		ordering = ['org_name']
		get_latest_by = 'created_date'
		verbose_name_plural = 'Salesforce Organizations'

	def __str__(self):
		result = [f'Org Id: {self.org_id}', f'Org Name: {self.org_name}',
				  f'Org Instance URL: {self.instance_url}', f'Package version installed: {self.package_version}']
		return ', '.join((str(x) for x in result))


class ClientOrg(models.Model):
	redditor = models.ForeignKey(
		Redditor, related_name='clients_orgs', on_delete=models.DO_NOTHING)
	salesforce_org = models.ForeignKey(
		SalesforceOrg, related_name='clients', on_delete=models.CASCADE)
	connected_at = models.DateTimeField(default=now)
	disconnected_at = models.DateTimeField(null=True)
	last_client_request_at = models.DateTimeField(null=True)
	last_client_update_at = models.DateTimeField(null=True)
	is_active = models.BooleanField(default=True)
	reddit_token = EncryptedCharField(
		max_length=256, null=True, help_text='Reddit refresh token for the Salesforce Client Org.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = MyModelManager()

	@property
	def is_authenticated(self):
		return self.__is_authenticated

	@is_authenticated.setter
	def is_authenticated(self, val):
		self.__is_authenticated = val

	class Meta:
		ordering = ['updated_at']
		get_latest_by = ['created_date']
		verbose_name_plural = "Salesforce Organizations Clients"

	def __str__(self):
		result = [f'Redditor Name: {self.redditor.name}',
				  f'Connected at: {self.connected_at}',
				  f'Disconnected at: {self.disconnected_at}',
				  f'Last client request at: {self.last_client_request_at}',
				  f'Last client update at: {self.last_client_update_at}',
				  f'Is active: {self.is_active}']
		return ', '.join((str(x) for x in result))

	def new_client_request(self):
		self.last_client_request_at = now()
		self.save()


class Token(models.Model):
	"""
	A Token model adapted to be used with the ClientOrg model instead of User
	"""
	key = models.CharField(_("Key"), max_length=40, primary_key=True)
	client_org = models.OneToOneField(
		ClientOrg, related_name='auth_token',
		on_delete=models.CASCADE, verbose_name=_("Client Org")
	)
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

	objects = MyModelManager()

	class Meta:
		# Work around for a bug in Django:
		# https://code.djangoproject.com/ticket/19422
		#
		# Also see corresponding ticket:
		# https://github.com/encode/django-rest-framework/issues/705
		# abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
		verbose_name = _("Token")
		verbose_name_plural = _("Tokens")

	def save(self, *args, **kwargs):
		if not self.key:
			self.key = self.generate_key()
		return super().save(*args, **kwargs)

	def generate_key(self):
		return binascii.hexlify(os.urandom(20)).decode()

	def __str__(self):
		return self.key
