Redditors
=========

All the endpoints provided to interact with Redditors for an authorized
client.

-  `Redditor details <#redditor-details>`__

Common Error Responses for Redditors endpoints:
-----------------------------------------------

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

Redditor details
----------------

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
