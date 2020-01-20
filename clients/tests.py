from rest_framework.test import APIClient, APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache

from herokuredditapi.utils import Utils
logger = Utils.init_logger(__name__)

class ClientsTests(APITestCase):
	state = None

	def oauth_helper(self):
		"""
		Helper function to test oauth endpoint
		"""
		url = reverse('clients:oauth')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.state = response.data['state']
		oauth_url = response.data['oauth_url']
		self.assertIn(self.state, oauth_url)

		self.assertTrue(cache.has_key(f'oauth_{self.state}'))
		oauth_data = cache.get(f'oauth_{self.state}')
		self.assertEqual(oauth_data['status'], 'pending')

	def oauth_callback_helper(self):
		"""
		Helper function to test oauth_callback endpoint
		"""
		pass







