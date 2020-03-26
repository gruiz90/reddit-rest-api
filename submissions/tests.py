from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from clients.utils import ClientsUtils


class SubmissionsTests(APITestCase):
    def setUp(self):
        # I need to insert a dummy client and add the token key in the client
        # credentials for authorizing all requests by the test client
        token_key = ClientsUtils.insert_dummy_client()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_key}')

    def _dummy_submission_request(self, path, post=False, delete=False):
        url = reverse(path, args=['1234567890'])
        if post:
            response = self.client.post(url)
        elif delete:
            response = self.client.delete(url)
        else:
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {
                'error': {
                    'code': 404,
                    'messages': [
                        'detail: No submission exists with the id: 1234567890.'
                    ],
                }
            },
        )

    def test_submission_info(self):
        """
        Function to test submission_info get endpoint when having the bearer token.
        I can use the read_only mod of reddit instance to get an actual submission data.
        """
        # First try with a dummy id to get 404 response
        self._dummy_submission_request('submissions:submission_info')

        # Now try with a real comment id
        url = reverse('submissions:submission_info', args=['78uvdw'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Python' in response.data['title'])

    def test_submission_info_delete(self):
        """
        Function to test submission_info delete endpoint when having the bearer token.
        I can use the read_only mod of reddit instance to get an actual submission data.
        """
        # First try with a dummy id to get 404 response
        self._dummy_submission_request('submissions:submission_info', delete=True)

        # Now try with a real submission id
        submission_id = '78uvdw'
        url = reverse('submissions:submission_info', args=[submission_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            f'Cannot delete submission with id: {submission_id}'
            in response.data['detail']
        )

    def test_submission_vote(self):
        """
        Function to test submission_vote endpoint when having the bearer token.
        I can't fully test this one as the reddit instance is read only.
        """
        self._dummy_submission_request('submissions:submission_vote', post=True)

        # Now try with a real comment id
        submission_id = '78uvdw'
        url = reverse('submissions:submission_vote', args=[submission_id])
        response = self.client.post(url, data={'vote_value': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['detail'],
            f'Vote action \'dummy\' successful for submission with id: {submission_id}.',
        )

    def test_submission_reply(self):
        """
        Function to test submission_reply endpoint.
        """
        self._dummy_submission_request('submissions:submission_reply', post=True)

        # Now try with a real submission id
        submission_id = '78uvdw'
        url = reverse('submissions:submission_reply', args=[submission_id])
        response = self.client.post(url, data={'body': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error']['messages'][0],
            'detail: The body must contain the comment in a Markdown format.',
        )

        response = self.client.post(url, data={'body': 'test'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            f'Cannot create comment in submission with id: {submission_id}'
            in response.data['detail']
        )

    def test_submission_crosspost(self):
        """
        Function to test submission_reply endpoint.
        """
        self._dummy_submission_request('submissions:submission_crosspost', post=True)

        # Now try with a real submission id
        submission_id = '78uvdw'
        url = reverse('submissions:submission_crosspost', args=[submission_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error']['messages'][0],
            'detail: A subreddit value corresponding to an existent subreddit name must be provided in the json data.',
        )

        subreddit_name = 'dummy_name'
        response = self.client.post(url, data={'subreddit': subreddit_name})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['error']['messages'][0],
            f'detail: No subreddit exists with the name: {subreddit_name}.',
        )

        response = self.client.post(url, data={'subreddit': 'test'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            f'Cannot create crosspost submission with id: {submission_id}'
            in response.data['detail']
        )

    def test_submission_comments(self):
        """
        Function to test submission_comments endpoint when having the bearer token.
        I can use the read_only mod of reddit instance to get actual data.
        """
        self._dummy_submission_request('submissions:submission_comments')

        # Now try with a real comment id
        url = reverse('submissions:submission_comments', args=['78uvdw'])
        response = self.client.get(
            url, {'sort': 'top', 'limit': 1, 'flat': True, 'offset': 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['comments']) == 1)
        self.assertTrue(response.data['sort_type'] == 'top' and response.data['flat'])
