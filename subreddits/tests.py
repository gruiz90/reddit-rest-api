from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from clients.utils import ClientsUtils
from .models import Subreddit
from clients.models import ClientOrg


class SubredditsTests(APITestCase):
    def setUp(self):
        # I need to insert a dummy client and add the token key in the client
        # credentials for authorizing all requests by the test client
        token_key = ClientsUtils.insert_dummy_client()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_key}')

    def _dummy_subreddit_request(self, path, post=False):
        url = reverse(path, args=['dummy_name'])
        if post:
            response = self.client.post(f'{url}')
        else:
            response = self.client.get(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {
                'error': {
                    'code': 404,
                    'messages': [
                        'detail: No subreddit exists with the name: dummy_name.'
                    ],
                }
            },
        )

    def test_subreddit_info(self):
        """
		Function to test subreddit_info endpoint when having the bearer token.
		I can use the read_only mod of reddit instance to get an actual subreddit data.
		"""
        # First try with a dummy name to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit_info')

        # Now try with a real subreddit name
        url = reverse('subreddits:subreddit_info', args=['Python'])
        response = self.client.get(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Python' in response.data['display_name'])

    def test_subreddit_subscriptions(self):
        """
		Function to test subreddit_subscriptions endpoint when having the bearer token.
		"""
        url = reverse('subreddits:subreddit_subscriptions')
        response = self.client.get(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['subscriptions']) == 0)

    def test_subreddit_rules(self):
        """
		Function to test subreddit_rules endpoint when having the bearer token.
		I can use the read_only mod of reddit instance to get an actual subreddit data.
		"""
        # First try with a dummy name to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit_rules')

        # Now try with a real subreddit name
        url = reverse('subreddits:subreddit_rules', args=['Python'])
        response = self.client.get(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['rules']) > 0)

    def test_subreddit_submissions(self):
        """
		Function to test subreddit_submissions endpoint when having the bearer token.
		I can use the read_only mod of reddit instance to get an actual subreddit data.
		"""
        # First try with a dummy name to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit_submissions')

        # Now try with a real subreddit name
        url = reverse('subreddits:subreddit_submissions', args=['Python'])
        offset = 5
        response = self.client.get(
            f'{url}', {'sort': 'top', 'time_filter': 'year', 'offset': offset}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['submissions']) < 6)
        self.assertTrue(
            response.data['sort_type'] == 'top' and response.data['offset'] == offset
        )

    def _subscribe_unsubscribe_request(self, action, action_msg):
        sub_name = 'Python'
        url = reverse(f'subreddits:subreddit_{action}', args=[sub_name])
        response = self.client.post(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        action_string = 'subscribe to' if action == 'subscribe' else 'unsubscribe from'
        self.assertEqual(
            response.data,
            {
                'detail': f'Reddit instance is read only. Cannot {action_string} subreddit r/{sub_name}.'
            },
        )

    def test_subreddit_subscribe_unsubscribe(self):
        """
		Function to test subreddit_subscribe and subreddit_unsubscribe endpoints 
		when having the bearer token.
		"""
        # First try with a dummy id to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit_subscribe', post=True)
        self._dummy_subreddit_request('subreddits:subreddit_unsubscribe', post=True)

        # Now try with a real subreddit name
        self._subscribe_unsubscribe_request('subscribe', 'subscribed to')
        self._subscribe_unsubscribe_request('unsubscribe', 'unsubscribed from')

    def test_subreddit_connect_disconnnect(self):
        """
		Function to test subreddit_connect and subreddit_disconnect endpoints 
		when having the bearer token.
		"""
        # First try with a dummy id to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit_connect', post=True)
        self._dummy_subreddit_request('subreddits:subreddit_disconnect', post=True)

        # Now try with a real subreddit name
        sub_name = 'Python'
        url = reverse(f'subreddits:subreddit_connect', args=[sub_name])
        response = self.client.post(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('Python' in response.data['display_name'])
        self.assertEqual(Subreddit.objects.count(), 1)
        self.assertEqual(
            Subreddit.objects.all()[0].clients.all()[0].salesforce_org_id,
            ClientOrg.objects.all()[0].salesforce_org_id,
        )

        url = reverse(f'subreddits:subreddit_disconnect', args=[sub_name])
        response = self.client.post(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'detail': 'Client disconnected subreddit succesfully.'}
        )
        self.assertTrue(Subreddit.objects.all()[0].clients.count() == 0)
