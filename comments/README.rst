Comments
========

All the endpoints provided to interact with Comments for an authorized
client.

-  `Comment Information <#comment-information>`__
-  `Comment Replies <#comment-replies>`__
-  `Comment Post Vote <#comment-vote>`__

Common Error Responses for Comments endpoints:
----------------------------------------------

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
                   "detail: No comment exists with the id: ???."
               ]
           }
       }

Comment Information
-------------------

Endpoint to get the Comment data by the id provided in the URL.

-  **URL**

   ``/comments/<str:id>``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/comments/faab0e4 \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "id": "faab0e4",
               "body": "This meme implies that we aren’t already allies with r/lotrmemes. If it weren’t for them we would’ve lost the great meme wars.",
               "created_utc": "2019-12-09T15:45:18",
               "author": {
                   "id": "fdqaa",
                   "name": "suckit5253",
                   "created_utc": "2014-02-21T13:19:49",
                   "icon_img": "https://www.redditstatic.com/avatars/avatar_default_15_DDBD37.png",
                   "comment_karma": 88502,
                   "link_karma": 60633
               },
               "score": 1466,
               "permalink": "/r/PrequelMemes/comments/e8a0c7/reddit_assemble/faab0e4/",
               "link_id": "t3_e8a0c7",
               "parent_id": "t3_e8a0c7",
               "submission": {
                   "id": "e8a0c7",
                   "name": "t3_e8a0c7",
                   "title": "Reddit assemble",
                   "created_utc": "2019-12-09T13:33:35",
                   "author_name": "starwarsgeek1985",
                   "num_comments": 455,
                   "score": 39006,
                   "url": "https://i.redd.it/kz7ku53k1m341.jpg"
               },
               "subreddit": {
                   "id": "3i60n",
                   "name": "t5_3i60n",
                   "display_name": "PrequelMemes",
                   "public_description": "Memes of the Star Wars Prequels",
                   "created_utc": "2016-12-27T03:05:47",
                   "subscribers": 1120894
               },
               "has_replies": true,
               "is_submitter": false,
               "distinguished": null,
               "edited": false,
               "stickied": false
           }
       }

Comment Replies
---------------

Endpoint to get a Comment's replies. It returns a max of 20 replies per
request. Uses offset to get the rest in different requests. The flat
parameter is used to retrieve replies with lower level than top level.
The order of the list with flat=True is [Reply\_Level1, Reply\_Level2,
..., Reply\_LevelN]

-  **URL**

   ``/comments/<str:id>/replies``

-  **Method:**

   ``GET``

-  **URL Params**

   **Optional:**

   ``limit=[0<int<21] (default=10)`` ``offset=[0<=int] (default=0)``
   ``flat=[True|False] (default=False)``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/comments/faab0e4/replies?limit=2&flat=True \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "replies": [
                   {
                       "id": "faadzi5",
                       "body": "*flashbacks to Meme War II*\n\nWhat a glorious and bloody battle that was, brother.",
                       "created_utc": "2019-12-09T16:05:39",
                       "author_name": "normiesreeeeeeee",
                       "score": 671,
                       "subreddit_id": "t5_3i60n",
                       "link_id": "t3_e8a0c7",
                       "parent_id": "t1_faab0e4",
                       "has_replies": true
                   },
                   {
                       "id": "faaxjgn",
                       "body": "This is a repost that first came up during the whole “r/prequelmemes is dying” thing earlier this year that ended up pushing the sub over a million subscribers. r/lotrmemes was a big reason for the jump in subscribers",
                       "created_utc": "2019-12-09T18:08:23",
                       "author_name": "landoofficial",
                       "score": 43,
                       "subreddit_id": "t5_3i60n",
                       "link_id": "t3_e8a0c7",
                       "parent_id": "t1_faab0e4",
                       "has_replies": true
                   }
               ],
               "limit_request": 2,
               "offset": 0,
               "flat": "True"
           }
       }

Comment Vote
------------

Endpoint to post a vote for a comment by the id provided in the url.
Passing vote\_value = [-1\|0\|1] a downvote, clear\_vote, upvote action
is executed for the submission.

-  **URL**

   ``/comment/<str:id>/vote``

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

       http POST https://reddit-rest-api.herokuapp.com/comment/faab0e4/vote \
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
