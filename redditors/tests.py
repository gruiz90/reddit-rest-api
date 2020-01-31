from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from redditors.utils import RedditorsUtils
from clients.utils import ClientsUtils


class RedditorsTests(APITestCase):
    def setUp(self):
        # I need to insert a dummy client and add the token key in the client
        # credentials for authorizing all requests by the test client
        token_key = ClientsUtils.insert_dummy_client()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_key}')

    def test_client_redditor(self):
        """
		Function to test my_redditor endpoint when having the bearer token
		"""
        url = reverse('redditors:my_redditor')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dummy_redditor = RedditorsUtils.get_dummy_redditor_data()
        dummy_redditor.update(subscriptions=[])
        self.assertEqual(response.data, dummy_redditor)

    def test_redditor_info(self):
        """
		Function to test redditor_info endpoint when having the bearer token.
		I can use the read_only mod of reddit instance to get accurate data.
		"""
        url = reverse('redditors:redditor_info', args=['sfdctest'])
        response = self.client.get(f'{url}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sfdctest', response.data.values())
