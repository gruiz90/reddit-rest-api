from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import praw
import random
import os
from django.shortcuts import redirect, Http404


class AccountOauthView(APIView):
    """
    API endpoint that starts the Reddit Account oauth flow
    """

    def get(self, request, Format=None):
        print('-' * 50)
        print('New Reddit Oauth login...')

        # redirectUri = request.query_params.get('redirect_uri')
        # orgId = request.query_params.get('org_id')
        # print(f'Redirect URI: {redirectUri}')
        # print(f'Org ID: {orgId}')

        state = request.query_params.get('state')
        code = request.query_params.get('code')

        if state:
            cookieState = request.COOKIES.get('state')
            print(f'State in cookie: {cookieState}')
            if cookieState is not None and state == cookieState:
                print(f'Code received: {code} ... What to do now???')
            else:
                raise Http404
        else:
            # Save in reddis the uri by orgId?
            # Response.set_cookie('redirectUriReddit', redirectUri)
            # print('Redirect URI stored in browser's cookies by key "redirectUriReddit"')
            redditClientId = os.environ.get('REDDIT_CLIENT_ID')
            print(f'Reddit client id: {redditClientId}')

            # Obtain authorization URL
            reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                                 client_secret=os.environ.get(
                                     'REDDIT_CLIENT_SECRET'),
                                 redirect_uri='http://localhost:8000/accounts',
                                 user_agent=os.environ.get('REDDIT_USER_AGENT'))
            state = str(random.randint(0, 65000))
            print(f'state generated: {state}')
            authUrl = reddit.auth.url(
                ['identity', 'mysubreddits', 'read', 'subscribe', 'vote'], state, 'permanent')
            print(f'Redirecting to -> {authUrl}')

            response = redirect(authUrl)
            response.set_cookie('state', state)
            print('Saved state in cookies for now..')
            return response
        return Response(status=status.HTTP_204_NO_CONTENT)
