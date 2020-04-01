Comments
========

All the endpoints provided to interact with Submission's Comments for an authorized
client.

-  `Comment details <#comment-details>`__
-  `Comment edit <#comment-edit>`__
-  `Comment delete <#comment-delete>`__
-  `Comment post vote <#comment-vote>`__
-  `Comment replies <#comment-replies>`__
-  `Comment post reply <#comment-post-reply>`__

Common error responses for Comments endpoints:
----------------------------------------------

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

Comment details
-------------------

Endpoint to get the Comment details by the id provided in the URL.

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

Comment edit
-------------------

Endpoint to edit a comment by the id provided in the URL.
The body is the Markdown formatted content for the comment.

-  **URL**

   ``/comments/<str:id>``

-  **Method:**

   ``PATCH``

-  **Data Params**

   **Required:**

   ``body=[string] -- Markdown formatted content``

   e.g:

   .. code:: json

       {
           "body": "**test**"
       }

-  **Sample Call:**

   .. code:: shell

       http PATCH https://reddit-rest-api.herokuapp.com/comments/flkv4st \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       body=**test**

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Comment 'flkv4st' successfully edited.",
                "comment": {
                    "id": "flkv4st",
                    "body": "**test**",
                    "created_utc": "2020-03-26T18:44:21",
                    "author": {
                        "id": "4rfkxa54",
                        "name": "sfdctest",
                        "created_utc": "2019-10-31T22:22:45",
                        "icon_img": "https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png",
                        "comment_karma": 3,
                        "link_karma": 26
                    },
                    "score": 0,
                    "permalink": "/r/test/comments/fpeo3h/tiny_monk/flkv4st/",
                    "link_id": "t3_fpeo3h",
                    "parent_id": "t1_flkkb46",
                    "submission": {
                        "id": "fpeo3h",
                        "name": "t3_fpeo3h",
                        "title": "Tiny monk",
                        "created_utc": "2020-03-26T16:37:22",
                        "author_name": "sfdctest",
                        "num_comments": 4,
                        "score": 18,
                        "url": "https://i.pinimg.com/originals/93/64/ef/9364efa9a8b36b0abe30870813af654f.gif"
                    },
                    "subreddit": {
                        "id": "2qh23",
                        "name": "t5_2qh23",
                        "display_name": "test",
                        "public_description": "",
                        "created_utc": "2008-01-25T05:11:28",
                        "subscribers": 7351
                    },
                    "has_replies": true,
                    "is_submitter": true,
                    "distinguished": null,
                    "edited": true,
                    "stickied": false
                }
            }
        }

-  **Error Response:**

   **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Cannot edit the comment with id: flkv4st. The authenticated reddit user u/sfdctest needs to be the same as the comment's author u/testuser",
                "comment": null
            }
        }

Comment delete
-------------------

Endpoint to delete a comment by the id provided in the URL.

-  **URL**

   ``/comments/<str:id>``

-  **Method:**

   ``DELETE``

-  **Sample Call:**

   .. code:: shell

       http DELETE https://reddit-rest-api.herokuapp.com/comments/fly4ow9 \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Comment 'fly4ow9' successfully deleted."
            }
        }

-  **Error Response:**

   **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Cannot delete the comment with id: flkv4st. The authenticated reddit user u/sfdctest needs to be the same as the comment's author u/testuser"
            }
        }

   **Code:** 404 Not Found **Content:**

   .. code:: json

        {
            "data": {
                "detail": "Cannot delete the comment with id: fly4ow9. The comment was already deleted or there is no way to verify the author at this moment."
            }
        }

Comment vote
------------

Endpoint to post a vote for a comment by the id provided in the url.
Passing vote\_value = [-1\|0\|1] a downvote, clear\_vote, upvote action
is executed for the submission.

-  **URL**

   ``/comments/<str:id>/vote``

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

       http POST https://reddit-rest-api.herokuapp.com/comments/flkv4st/vote \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       vote_value=1

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Vote action 'Upvote' successful for comment with id: flkv4st.",
                "comment": {
                    "id": "flkv4st",
                    "body": "test2",
                    "created_utc": "2020-03-26T18:44:21",
                    "author_name": "sfdctest",
                    "score": 0,
                    "subreddit_id": "t5_2qh23",
                    "link_id": "t3_fpeo3h",
                    "parent_id": "t1_flkkb46",
                    "has_replies": true
                }
            }
        }

Comment replies
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

Comment post reply
------------------

Endpoint that allows posting a reply to a comment by the id provided in the URL.
The body is the Markdown formatted content for the comment.

-  **URL**

   ``/comments/<str:id>/replies``

-  **Method:**

   ``POST``

-  **Data Params**

   **Required:**

   ``body=[string] -- Markdown formatted content``

   e.g:

   .. code:: json

       {
           "body": "# test"
       }

-  **Sample Call:**

   .. code:: shell

       http POST https://reddit-rest-api.herokuapp.com/comments/flkv4st/replies \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       body=# test

-  **Success Response:**

-  **Code:** 201 Created **Content:**

   .. code:: json

       {
            "data": {
                "detail": "New reply posted by u/sfdctest with id 'fm37apt' to comment with id: flkv4st",
                "comment": {
                    "id": "fm37apt",
                    "body": "# test",
                    "created_utc": "2020-04-01T04:19:17",
                    "author": {
                        "id": "4rfkxa54",
                        "name": "sfdctest",
                        "created_utc": "2019-10-31T22:22:45",
                        "icon_img": "https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png",
                        "comment_karma": 3,
                        "link_karma": 26
                    },
                    "score": 1,
                    "permalink": "/r/test/comments/fpeo3h/tiny_monk/fm37apt/",
                    "link_id": "t3_fpeo3h",
                    "parent_id": "t1_flkv4st",
                    "submission": {
                        "id": "fpeo3h",
                        "name": "t3_fpeo3h",
                        "title": "Tiny monk",
                        "created_utc": "2020-03-26T16:37:22",
                        "author_name": "sfdctest",
                        "num_comments": 5,
                        "score": 18,
                        "url": "https://i.pinimg.com/originals/93/64/ef/9364efa9a8b36b0abe30870813af654f.gif"
                    },
                    "subreddit": {
                        "id": "2qh23",
                        "name": "t5_2qh23",
                        "display_name": "test",
                        "public_description": "",
                        "created_utc": "2008-01-25T05:11:28",
                        "subscribers": 7351
                    },
                    "has_replies": false,
                    "is_submitter": true,
                    "distinguished": null,
                    "edited": false,
                    "stickied": false
                }
            }
        }
