from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from clients.utils import ClientsUtils


class CommentsTests(APITestCase):
    def setUp(self):
        # I need to insert a dummy client and add the token key in the client
        # credentials for authorizing all requests by the test client
        token_key = ClientsUtils.insert_dummy_client()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_key}')

    def _dummy_comment_request(self, path, post=False, patch=False, delete=False):
        url = reverse(path, args=['1234567890'])
        if post:
            response = self.client.post(url)
        elif patch:
            response = self.client.patch(url)
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
                    'messages': ['detail: No comment exists with the id: 1234567890.'],
                }
            },
        )

    def test_comment_details(self):
        """
        Function to test comment endpoint when having the bearer token.
        I can use the read_only mod of reddit instance to get an actual comment data.
        """
        # First try with a dummy id to get 404 response
        self._dummy_comment_request('comments:comment')

        # Now try with a real comment id
        url = reverse('comments:comment', args=['faab0e4'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('meme' in response.data['body'])

    def test_comment_edit(self):
        """
        Function to test comment patch endpoint.
        """
        # First try with a dummy id to get 404 response
        self._dummy_comment_request('comments:comment', patch=True)

        # Now try with a real comment id
        comment_id = 'faab0e4'
        url = reverse('comments:comment', args=[comment_id])
        response = self.client.patch(url, data={'body': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error']['messages'][0],
            'detail: The body must contain the comment in a Markdown formatted format.',
        )

        response = self.client.patch(url, data={'body': 'test'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            f'Cannot edit comment with id: {comment_id}.' in response.data['detail']
        )

    def test_comment_delete(self):
        """
        Function to test comment delete endpoint.
        """
        # First try with a dummy id to get 404 response
        self._dummy_comment_request('comments:comment', delete=True)

        # Now try with a real comment id
        comment_id = 'faab0e4'
        url = reverse('comments:comment', args=[comment_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            f'Cannot delete comment with id: {comment_id}.' in response.data['detail']
        )

    def test_comment_vote(self):
        """
        Function to test comment_vote endpoint when having the bearer token.
        I can't fully test this one as the reddit instance is read only.
        """
        self._dummy_comment_request('comments:comment_vote', post=True)

        # Now try with a real comment id
        comment_id = 'faab0e4'
        url = reverse('comments:comment_vote', args=[comment_id])
        response = self.client.post(url, data={'vote_value': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['detail'],
            f'Vote action \'dummy\' successful for comment with id: {comment_id}.',
        )

    def test_comment_reply(self):
        """
        Function to test post comment_replies endpoint.
        """
        self._dummy_comment_request('comments:comment_replies', post=True)

        # Now try with a real comment id
        comment_id = 'faab0e4'
        url = reverse('comments:comment_replies', args=[comment_id])
        response = self.client.post(url, data={'body': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error']['messages'][0],
            'detail: The body must contain the comment in a Markdown formatted format.',
        )

        response = self.client.post(url, data={'body': 'test'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            f'Cannot create reply to comment with id: {comment_id}.'
            in response.data['detail']
        )

    def test_comment_replies(self):
        """
        Function to test comment_replies endpoint when having the bearer token.
        I can use the read_only mod of reddit instance to get actual data.
        """
        self._dummy_comment_request('comments:comment_replies')

        # Now try with a real comment id
        url = reverse('comments:comment_replies', args=['faab0e4'])
        response = self.client.get(url, {'limit': 1, 'flat': True, 'offset': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['replies']) == 1)
