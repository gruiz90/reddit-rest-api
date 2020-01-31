Redditors
=========

All the endpoints provided to interact with Redditors for an authorized
client.

-  `My Redditor Information <#my-redditor-info>`__
-  `Get Redditor Information <#get-redditor-info>`__

Common Error Responses for Redditors endpoints:
-----------------------------------------------

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
                   "detail: No redditor exists with the name: ???."
               ]
           }
       }

My Redditor Info
----------------

Endpoint to get the authorized reddit account redditor data and
subscriptions.

-  **URL**

   ``/redditors``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/redditors/sfdctest \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "id": "4rfkxa54",
               "name": "sfdctest",
               "created_utc": "2019-10-31T22:22:45Z",
               "has_verified_email": true,
               "icon_img": "https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png",
               "comment_karma": 0,
               "link_karma": 1,
               "num_friends": 0,
               "is_employee": false,
               "is_friend": false,
               "is_mod": false,
               "is_gold": false,
               "subscriptions": [
                   {
                       "id": "2r7yd",
                       "name": "t5_2r7yd",
                       "display_name": "learnprogramming",
                       "public_description": "A subreddit for all questions related to programming in any language.",
                       "created_utc": "2009-09-24T04:25:37",
                       "subscribers": 1186419
                   },
                   {
                       "id": "3i60n",
                       "name": "t5_3i60n",
                       "display_name": "PrequelMemes",
                       "public_description": "Memes of the Star Wars Prequels",
                       "created_utc": "2016-12-27T03:05:47",
                       "subscribers": 1120853
                   }
               ]
           }
       }

Get Redditor Info
-----------------

Endpoint to get the Redditor data by the name provided in the URL.

-  **URL**

   ``/redditors/<str:name>``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/redditors/sfdctest \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "id": "4rfkxa54",
               "name": "sfdctest",
               "created_utc": "2019-10-31T22:22:45",
               "has_verified_email": true,
               "icon_img": "https://www.redditstatic.com/avatars/avatar_default_09_A06A42.png",
               "comment_karma": 0,
               "link_karma": 1,
               "num_friends": 0,
               "is_employee": false,
               "is_friend": false,
               "is_mod": false,
               "is_gold": false
           }
       }
