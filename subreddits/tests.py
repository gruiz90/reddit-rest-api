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

    def _dummy_subreddit_request(self, path, subs=False, post=False, delete=False):
        url = reverse(path, args=[] if subs else ['dummy_name'])
        if post:
            response = self.client.post(url, data={'subreddit': 'dummy_name'})
        elif delete:
            response = self.client.delete(url, data={'subreddit': 'dummy_name'})
        else:
            response = self.client.get(url)
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

    def test_subreddit(self):
        """
        Function to test subreddit endpoint when having the bearer token.
        I can use the read_only mod of reddit instance to get an actual subreddit data.
        """
        # First try with a dummy name to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit')

        # Now try with a real subreddit name
        url = reverse('subreddits:subreddit', args=['test'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('test' in response.data['display_name'])

    def test_subreddit_subscriptions(self):
        """
        Function to test subreddit_subscriptions endpoint when having the bearer token.
        """
        url = reverse('subreddits:subscriptions')
        response = self.client.get(url)
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
        response = self.client.get(url)
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
        url = reverse('subreddits:subreddit_submissions', args=['test'])
        offset = 5
        response = self.client.get(
            url, {'sort': 'top', 'time_filter': 'year', 'offset': offset}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['submissions']) < 6)
        self.assertTrue(
            response.data['sort_type'] == 'top' and response.data['offset'] == offset
        )

    def _subscribe_unsubscribe_request(self, action='subscribe'):
        url = reverse(f'subreddits:subscriptions')
        if action == 'subscribe':
            response = self.client.post(url, data={'subreddit': 'test'})
        else:
            response = self.client.delete(url, data={'subreddit': 'test'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        action_string = 'subscribe to' if action == 'subscribe' else 'unsubscribe from'
        self.assertEqual(
            response.data['detail'],
            f'Reddit instance is read only. Cannot {action_string} subreddit r/test.',
        )

    def test_subreddit_subscribe_unsubscribe(self):
        """
        Function to test subreddit_subscribe and subreddit_unsubscribe endpoints 
        when having the bearer token.
        """
        # First try with a dummy id to get 404 response
        self._dummy_subreddit_request('subreddits:subscriptions', subs=True, post=True)
        self._dummy_subreddit_request(
            'subreddits:subscriptions', subs=True, delete=True
        )

        # Now try with a real subreddit name
        self._subscribe_unsubscribe_request()
        self._subscribe_unsubscribe_request(action='unsubscribe')

    def test_subreddit_submission(self):
        """
        Function to test POST in subreddit_submissions.
        """
        # First try with a dummy id to get 404 response
        self._dummy_subreddit_request('subreddits:subreddit_submissions', post=True)

        # Now try with a real subreddit name only with a title value
        url = reverse(f'subreddits:subreddit_submissions', args=['test'])
        response = self.client.post(url, data={'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error']['messages'][0],
            'detail: Either a selftext, url, image_path or video_path must be provided in the json data.',
        )

        response = self.client.post(url, data={'title': 'test', 'selftext': 'test'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            'Cannot submit a post creation in r/test.' in response.data['detail']
        )
