from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache
from .models import SalesforceOrg, ClientOrg, Token
from .utils import ClientsUtils
from redditors.utils import RedditorsUtils


class ClientsOauthTests(APITestCase):

	def _oauth(self):
		"""
		Function to test oauth endpoint
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

	def _oauth_callback(self):
		"""
		Function to test oauth_callback endpoint
		"""
		url = reverse('clients:oauth_callback')
		response = self.client.get(url, {'state': self.state, 'code': 'dummy'})
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)

	def _oauth_confirm_pending(self):
		"""
		Function to test oauth_confirm endpoint when status pending
		"""
		url = reverse('clients:oauth_confirm')
		response = self.client.get(url, {'state': self.state})
		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
		self.assertEqual(response.data, {'detail': 'Authorization still pending.'})

		# Check cache for oauth_data status
		self.assertTrue(cache.has_key(f'oauth_{self.state}'))
		oauth_data = cache.get(f'oauth_{self.state}')
		self.assertEqual(oauth_data['status'], 'pending')

	def _oauth_confirm_accepted(self):
		"""
		Function to test oauth_confirm endpoint when status accepted
		"""
		url = reverse('clients:oauth_confirm')
		response = self.client.get(url, {'state': self.state})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			response.data, {'result': 'accepted', 'detail': 'Authorization complete.'})

		# Check cache for oauth_data status
		self.assertTrue(cache.has_key(f'oauth_{self.state}'))
		oauth_data = cache.get(f'oauth_{self.state}')
		self.assertEqual(oauth_data['status'], 'accepted')
		self.assertEqual(oauth_data['code'], 'dummy')

	def _oauth_confirm_post(self):
		"""
		Function to test oauth_confirm endpoint when status accepted
		"""
		url = reverse('clients:oauth_confirm')
		response = self.client.post(
			f'{url}?state={self.state}',
			{'org_id': '1234567890', 'org_name': 'dummy'},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('sfdctest', response.data.values())

		# Check that oauth_data was deleted from cache
		self.assertFalse(cache.has_key(f'oauth_{self.state}'))
		# Check that the salesforce org was inserted
		self.assertTrue(SalesforceOrg.objects.count() == 1)
		self.assertTrue(SalesforceOrg.objects.all()[0].org_id == '1234567890')

	def test_oauth(self):
		self._oauth()
		self._oauth_confirm_pending()
		self._oauth_callback()
		self._oauth_confirm_accepted()
		self._oauth_confirm_post()


class ClientsDataTests(APITestCase):

	def setUp(self):
		# I need to insert a dummy client and add the token key in the client
		# credentials for authorizing all requests by the test client
		token_key = ClientsUtils.insert_dummy_client()
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_key}')

	def test_me(self):
		"""
		Function to test me endpoint when having the bearer token
		"""
		url = reverse('clients:me')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		dummy_redditor = RedditorsUtils.get_dummy_redditor_data()
		dummy_redditor.update(subscriptions=[])
		self.assertEqual(response.data, dummy_redditor)

	def test_disconnect(self):
		"""
		Function to test disconnect endpoint when having the bearer token
		"""
		url = reverse('clients:disconnect')
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, {'detail': 'Account disconnected succesfully.'})
		self.assertFalse(ClientOrg.objects.all()[0].is_active)
		self.assertTrue(Token.objects.count() == 0)
