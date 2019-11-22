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
    org_url = models.URLField(max_length=512)
    package_version = models.CharField(max_length=8, blank=True, default='1.0')

    objects = MyModelManager()

    class Meta:
        ordering = ['org_name']

    def __str__(self):
        result = [f'Org Id: {self.org_id}', f'Org Name: {self.org_name}',
                  f'Org URL: {self.org_url}', f'Package version installed: {self.package_version}']
        return ', '.join((str(x) for x in result))


class ClientOrg(models.Model):
    redditor = models.OneToOneField(
        Redditor, on_delete=models.CASCADE, related_name='client_org', primary_key=True)
    salesforce_org = models.ForeignKey(
        SalesforceOrg, related_name='clients', on_delete=models.CASCADE)
    timestamp_client_connected = models.DateTimeField(
        auto_now=False, auto_now_add=False, default=now)
    timestamp_client_disconnected = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    last_time_client_request = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    last_time_client_updated = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    reddit_token = EncryptedCharField(
        max_length=256, help_text='Reddit refresh token for the Salesforce Client Org.')
    client_token = EncryptedCharField(
        max_length=256, help_text='Generated random token for Salesforce Client Org.')

    objects = MyModelManager()

    class Meta:
        ordering = ['timestamp_client_connected']

    def __str__(self):
        result = [f'Connection timestamp: {self.timestamp_client_connected}',
                  f'Disconnection timestamp: {self.timestamp_client_disconnected}',
                  f'Client request timestamp: {self.last_time_client_request}',
                  f'Client update timestamp: {self.last_time_client_updated}']
        return ', '.join((str(x) for x in result))


class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    client_org = models.OneToOneField(
        ClientOrg, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("Client Org")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    objects = MyModelManager()

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
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
