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

    def _dummy_submission_request(self, path, post=False):
        url = reverse(path, args=['1234567890'])
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
                        'detail: No submission exists with the id: 1234567890.'
                    ],
                }
            },
        )

    def test_submission_info(self):
        """
		Function to test submission_info endpoint when having the bearer token.
		I can use the read_only mod of reddit instance to get an actual submission data.
		"""
        # First try with a dummy id to get 404 response
        self._dummy_submission_request('submissions:submission_info')

        # Now try with a real comment id
        url = reverse('submissions:submission_info', args=['78uvdw'])
        response = self.client.get(f'{url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Python' in response.data['title'])

    def test_comment_vote(self):
        """
		Function to test comment_vote endpoint when having the bearer token.
		I can't fully test this one as the reddit instance is read only.
		"""
        self._dummy_submission_request('submissions:submission_vote', post=True)

        # Now try with a real comment id
        submission_id = '78uvdw'
        url = reverse('submissions:submission_vote', args=[submission_id])
        response = self.client.post(f'{url}', data={'vote_value': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'detail': f'Vote action \'dummy\' successful for submission with id: {submission_id}!'
            },
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
            f'{url}', {'sort': 'top', 'limit': 1, 'flat': True, 'offset': 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['comments']) == 1)
        self.assertTrue(response.data['sort_type'] == 'top' and response.data['flat'])
