Submissions
===========

All the endpoints provided to interact with Submissions for an
authorized client.

-  `Submission Information <#submission-information>`__
-  `Submission Comments <#submission-comments>`__
-  `Submission Post Vote <#submission-vote>`__

Common Error Responses for Submissions endpoints:
-------------------------------------------------

-  **Code:** 401 Unauthorized **Content:**

   .. code:: json

       {
           "error": {
               "code": 401,
               "messages": [
                   "detail: Authentication credentials were not provided."
               ]
           }
       }

   OR

-  **Code:** 401 Unauthorized **Content:**

   .. code:: json

       {
           "error": {
               "code": 401,
               "messages": [
                   "detail: Invalid token."
               ]
           }
       }

   OR

-  **Code:** 404 Not Found **Content:**

   .. code:: json

       {
           "error": {
               "code": 404,
               "messages": [
                   "detail: No submission exists with the id: ???."
               ]
           }
       }

Submission Information
----------------------

Endpoint to get the Submission data by the id provided in the URL.

-  **URL**

   ``/submissions/<str:id>``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/submissions/e8ge80 \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "id": "e8ge80",
               "name": "t3_e8ge80",
               "title": "PRAW - Reddit API",
               "created_utc": "2019-12-09T21:31:13",
               "author": {
                   "id": "12pod7",
                   "name": "NewbieWithARuby",
                   "created_utc": "2016-11-10T01:47:15",
                   "icon_img": "https://www.redditstatic.com/avatars/avatar_default_08_FF66AC.png",
                   "comment_karma": 97946,
                   "link_karma": 6211
               },
               "num_comments": 0,
               "score": 1,
               "upvote_ratio": 1.0,
               "permalink": "/r/Python/comments/e8ge80/praw_reddit_api/",
               "url": "https://www.reddit.com/r/Python/comments/e8ge80/praw_reddit_api/",
               "is_original_content": false,
               "is_self": true,
               "selftext": "I'm having some trouble with PRAW, the Reddit API.\n\nIf I get a list of the 100 'Hot' posts on r/python using:\n\n>sub = r.subreddit('python')\n\n>posts = sub.hot(limit=100)\n\n\nAnd then I take one of those posts, i.e.\n\n>posts[0]\n\n>*Output*》Submission(id='a1b2c3')\n\nThen the post has a number of attributes, specifically the one I'm interested in being:\n\n>posts[0].media\n\nBut if I instead do:\n\n>some_post = r.submission(id='a1b2c3')\n\n>*Output*》Submission(id='a1b2c3')\n\nI no longer get the attribute .media available.\n\nWhat am I doing wrong here?",
               "clicked": false,
               "distinguished": null,
               "edited": false,
               "locked": false,
               "stickied": false,
               "spoiler": false,
               "over_18": false
           }
       }

Submission Comments
-------------------

Endpoint to get a Submission's comments. It returns a max of 20 comments
per request. Uses offset to get the rest in different requests. The flat
parameter is used to retrieve comments with lower level than top level.
The order of the list with flat=True is [Comments\_Level1,
Comments\_Level2, ..., Comments\_LevelN]

-  **URL**

   ``/submissions/<str:id>/comments``

-  **Method:**

   ``GET``

-  **URL Params**

   **Optional:**

   ``sort=[best|top|new|controversial|old|q_a] (default=best)``
   ``limit=[0<int<21] (default=10)`` ``offset=[0<=int] (default=0)``
   ``flat=[True|False] (default=False)``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/submissions/e7t00m/comments?sort=top&limit=2&offset=3 \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "comments": [
                   {
                       "id": "fa5o7ul",
                       "body": "In qr-filetransfer/qr-filetransfer why is there a class inside a function ? What is the benefit of doing this ?",
                       "created_utc": "2019-12-08T14:55:55",
                       "author_name": "reJectedeuw",
                       "score": 13,
                       "subreddit_id": "t5_2qh0y",
                       "link_id": "t3_e7t00m",
                       "parent_id": "t3_e7t00m",
                       "has_replies": true
                   },
                   {
                       "id": "fa58he7",
                       "body": "What is the advantage of this over something like KDE Connect? Lighter (I assume) and no need to pair, but you need scan a QR code and to use a web browser to pick flies which looks a bit clunky to me.",
                       "created_utc": "2019-12-08T13:44:08",
                       "author_name": "graemep",
                       "score": 21,
                       "subreddit_id": "t5_2qh0y",
                       "link_id": "t3_e7t00m",
                       "parent_id": "t3_e7t00m",
                       "has_replies": true
                   }
               ],
               "sort_type": "top",
               "limit_request": 2,
               "offset": 3,
               "flat": false
           }
       }

Submission Vote
---------------

Endpoint to post a vote for a submission by the id provided in the url.
Passing vote\_value = [-1\|0\|1] a downvote, clear\_vote, upvote action
is executed for the submission.

-  **URL**

   ``/submissions/<str:id>/vote``

-  **Method:**

   ``POST``

-  **Data Params**

   **Required:**

   ``vote_value=[-1<=int<=1]``

   e.g:

   .. code:: json

       {
           "vote_value": 1
       }

-  **Sample Call:**

   .. code:: shell

       http POST https://reddit-rest-api.herokuapp.com/submissions/e8a0c7/vote \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       vote_value=1

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "detail": "Vote action 'Upvote' successful for submission with id: e8a0c7!"
           }
       }
