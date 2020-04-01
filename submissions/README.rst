Submissions
===========

All the endpoints provided to interact with Submissions for an
authorized client.

-  `Submission details <#submission-details>`__
-  `Submission delete <#submission-delete>`__
-  `Submission post vote <#submission-vote>`__
-  `Submission crosspost <#submission-crosspost>`__
-  `Submission comments <#submission-comments>`__
-  `Submission post comment <#submission-post-comment>`__

Common error responses for Submissions endpoints:
-------------------------------------------------

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

Submission details
------------------

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

Submission delete
-----------------

Endpoint to delete a submission by the id provided in the URL.

-  **URL**

   ``/submissions/<str:id>``

-  **Method:**

   ``DELETE``

-  **Sample Call:**

   .. code:: shell

       http DELETE https://reddit-rest-api.herokuapp.com/submissions/e8ge80 \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Submission 'e8ge80' successfully deleted."
            }
        }

-  **Error Response:**

   **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Cannot delete the submission with id: e8ge80. The authenticated reddit user u/sfdctest needs to be the same as the submission's author u/testuser"
            }
        }

   **Code:** 404 Not Found **Content:**

   .. code:: json

        {
            "data": {
                "detail": "Cannot delete the submission with id: e8ge80. The submission was already deleted or there is no way to verify the author at this moment."
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

       http POST https://reddit-rest-api.herokuapp.com/submissions/fsuibu/vote \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       vote_value=1

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
            "data": {
                "detail": "Vote action 'Upvote' successful for submission with id: fsuibu.",
                "submission": {
                    "id": "fsuibu",
                    "name": "t3_fsuibu",
                    "title": "Maze Solver Visualizer - Dijkstra's algorithm (asynchronous neighbours)",
                    "created_utc": "2020-04-01T06:49:15",
                    "author_name": "mutatedllama",
                    "num_comments": 64,
                    "score": 1399,
                    "url": "https://v.redd.it/xb71rqy5l5q41"
                }
            }
        }

Submission crosspost
--------------------

Endpoint that allows API endpoint to crosspost a submission (by the name provided in the URL) to a target subreddit.

-  **URL**

   ``/submissions/<str:id>/crosspost``

-  **Method:**

   ``POST``

-  **Data Params**

   **Required:**

   ``subreddit=[string] –- Name of the subreddit or Subreddit object to crosspost into.``

   **Optional:**

   ``title=[string] –- Title of the submission. Will use this submission’s title if None (default: None).``

   ``flair_id=[string] -- The flair template to select (default: None)``

   ``flair_text=[string] -- If the template’s flair_text_editable value is True, this value will set a custom text (default: None).``

   ``send_replies=[bool] -- When True, messages will be sent to the submission author when comments are made to the submission (default: True).``

   ``nsfw=[bool] -- Whether or not the submission should be marked NSFW (default: False).``

   ``spoiler=[bool] -- Whether or not the submission should be marked as a spoiler (default: False).``

   e.g:

   .. code:: json

       {
            "subreddit": "test",
            "title": "Test crosspost",
            "send_replies": true,
            "spoiler": true
        }

-  **Sample Call:**

   .. code:: shell

       http POST https://reddit-rest-api.herokuapp.com/submissions/fsuibu/crosspost \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       subreddit='test' title='Test crosspost' \
       send_replies=true spoiler=true

-  **Success Response:**

-  **Code:** 201 Created **Content:**

   .. code:: json

       {
            "data": {
                "detail": "New crosspost submission created in r/test by u/sfdctest with id: ft86wd.",
                "cross_submission": {
                    "id": "ft86wd",
                    "name": "t3_ft86wd",
                    "title": "Test crosspost",
                    "created_utc": "2020-04-01T20:41:47",
                    "author": {
                        "id": "4rfkxa54",
                        "name": "sfdctest",
                        "created_utc": "2019-10-31T22:22:45",
                        "icon_img": "https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png",
                        "comment_karma": 3,
                        "link_karma": 26
                    },
                    "num_comments": 0,
                    "score": 1,
                    "upvote_ratio": 1.0,
                    "permalink": "/r/test/comments/ft86wd/test_crosspost/",
                    "url": "https://v.redd.it/xb71rqy5l5q41",
                    "is_original_content": false,
                    "is_self": false,
                    "selftext": "",
                    "clicked": false,
                    "distinguished": null,
                    "edited": false,
                    "locked": false,
                    "stickied": false,
                    "spoiler": true,
                    "over_18": false
                }
            }
        }

Submission comments
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

Submission post comment
-----------------------

Endpoint that allows posting a comment into a submission by the id provided in the URL.
The body is the Markdown formatted content for the comment.

-  **URL**

   ``/submissions/<str:id>/comments``

-  **Method:**

   ``POST``

-  **Data Params**

   **Required:**

   ``body=[string] -- Markdown formatted content``

   e.g:

   .. code:: json

       {
           "body": "~~testing~~"
       }

-  **Sample Call:**

   .. code:: shell

       http POST https://reddit-rest-api.herokuapp.com/submissions/fpeo3h/comments \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       body='~~testing~~'

-  **Success Response:**

-  **Code:** 201 Created **Content:**

   .. code:: json

       {
            "data": {
                "detail": "New comment posted by u/sfdctest with id 'fm56u4x' to submission with id: fpeo3h",
                "comment": {
                    "id": "fm56u4x",
                    "body": "~~testing~~",
                    "created_utc": "2020-04-01T18:56:39",
                    "author": {
                        "id": "4rfkxa54",
                        "name": "sfdctest",
                        "created_utc": "2019-10-31T22:22:45",
                        "icon_img": "https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png",
                        "comment_karma": 3,
                        "link_karma": 26
                    },
                    "score": 1,
                    "permalink": "/r/test/comments/fpeo3h/tiny_monk/fm56u4x/",
                    "link_id": "t3_fpeo3h",
                    "parent_id": "t3_fpeo3h",
                    "submission": {
                        "id": "fpeo3h",
                        "name": "t3_fpeo3h",
                        "title": "Tiny monk",
                        "created_utc": "2020-03-26T16:37:22",
                        "author_name": "sfdctest",
                        "num_comments": 6,
                        "score": 19,
                        "url": "https://i.pinimg.com/originals/93/64/ef/9364efa9a8b36b0abe30870813af654f.gif"
                    },
                    "subreddit": {
                        "id": "2qh23",
                        "name": "t5_2qh23",
                        "display_name": "test",
                        "public_description": "",
                        "created_utc": "2008-01-25T05:11:28",
                        "subscribers": 7352
                    },
                    "has_replies": false,
                    "is_submitter": true,
                    "distinguished": null,
                    "edited": false,
                    "stickied": false
                }
            }
        }
