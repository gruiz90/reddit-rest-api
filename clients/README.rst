Clients Authorization
=====================

All this endpoints provided ways to authorize/revoke access to client's Reddit Account, 
view client details and connect Salesforce orgs.

-  `OAuth init <#client-oauth>`__
-  `OAuth callback <#client-oauth-callback>`__
-  `OAuth status <#client-check-oauth-status>`__
-  `OAuth confirm <#client-confirm-authorization>`__
-  `Client details <#client-details>`__
-  `Client disconnect <#client-disconnect>`__
-  `Salesforce OAuth init <#salesforce-oauth>`__
-  `Salesforce OAuth callback <#salesforce-oauth-callback>`__
-  `Salesforce save token <#salesforce-save-token>`__
-  `Salesforce revoke token <#salesforce-revoke-token>`__

Client Oauth
------------

Initiates the Reddit Account oauth flow.

-  **URL**

   ``/clients/oauth``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/clients/oauth

-  **Success Response:**

-  **Code:** 200 **Content:**

   .. code:: json

       {
           "data": {
               "oauth_url": "https://www.reddit.com/api/v1/authorize?client_id=PJzoDgMB6HJUDA&duration=permanent&redirect_uri=https%3A%2F%2Freddit-rest-api.herokuapp.com%2Foauth_callback&response_type=code&scope=%2A&state=54221",
               "state": "54221"
           }
       }

Client Oauth Callback
---------------------

Handles the callback from the Reddit Oauth flow. Only used when the user
'allows' or 'declines' the conditions in the reddit authorization page.

-  **URL**

   ``/clients/oauth_callback``

-  **Method:**

   ``GET``

-  **URL Params**

   **Required:**

   ``state=[integer]`` ``code=[string]``

   **Optional:**

   ``error=[integer]``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback?state=11562&code=_TvTWeuxQI8YQ_eZE-7bfbc0QmI

-  **Success Response:**

-  **Code:** 200 **Content:**

   .. code:: json

       {
           "data": {
               "detail": "Oauth code saved successfully."
           }
       }

-  **Error Response:**

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback``
   **Code:** 400 Bad Request **Content:**

   .. code:: json

       {
           "error": {
               "code": 400,
               "messages": [
                   "detail: state param not found."
               ]
           }
       }

   OR

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback?state=abc``
   **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
           "error": {
               "code": 403,
               "messages": [
                   "detail: Invalid or expired state."
               ]
           }
       }

   OR

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback?state=11562&error=access_denied``
   **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
           "error": {
               "code": 403,
               "messages": [
                   "detail: access_denied"
               ]
           }
       }

Client check oauth status
-------------------------

Check oauth status for a Salesforce organization client.

-  **URL**

   ``/clients/oauth_confirm``

-  **Method:**

   ``GET``

-  **URL Params**

   **Required:**

   ``state=[integer]``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/clients/oauth_confirm?state=11562

-  **Success Response:**

-  **Code:** 202 **Content:**

   .. code:: json

       {
           "data": {
               "detail": "Authorization still pending."
           }
       }

   OR

   -  **Code:** 200 **Content:**

   .. code:: json

       {
           "data": {
               "result": "accepted",
               "detail": "Authorization complete."
           }
       }

   OR

   -  **Code:** 200 **Content:**

   .. code:: json

       {
           "data": {
               "result": "error",
               "detail": "access_denied"
           }
       }

-  **Error Response:**

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/oauth_confirm``
   **Code:** 400 Bad Request **Content:**

   .. code:: json

       {
           "error": {
               "code": 400,
               "messages": [
                   "detail: state param not found."
               ]
           }
       }

   OR

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/oauth_confirm?state=abc``
   **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
           "error": {
               "code": 403,
               "messages": [
                   "detail: Invalid or expired state."
               ]
           }
       }

Client confirm authorization
----------------------------

Handles the autorization confirmation of a Reddit account for a
Salesforce organization

-  **URL**

   ``/clients/oauth_confirm``

-  **Method:**

   ``POST``

-  **URL Params**

   **Required:**

   ``state=[integer]``

-  **Data Params**

   **Required:**

   ``org_id=[string]`` ``org_name=[string]``

   **Optional:** ``package_version=[string]``

   e.g:

   .. code:: json

       {
           "org_id": "testorgid",
           "org_name": "test",
           "package_version":"1.0"
       }

-  **Sample Call:**

   .. code:: shell

       http POST https://reddit-rest-api.herokuapp.com/clients/oauth_confirm?state=11562 \
       org_id=testorgid org_name=test package_version=1.0

-  **Success Response:**

-  **Code:** 201 Created **Content:**

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
                       "id": "2qh0y",
                       "name": "t5_2qh0y",
                       "display_name": "Python",
                       "public_description": "news about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
                       "created_utc": "2008-01-25T03:14:39",
                       "subscribers": 462393
                   },
                   {
                       "id": "2r7yd",
                       "name": "t5_2r7yd",
                       "display_name": "learnprogramming",
                       "public_description": "A subreddit for all questions related to programming in any language.",
                       "created_utc": "2009-09-24T04:25:37",
                       "subscribers": 1179032
                   },
                   {
                       "id": "3i60n",
                       "name": "t5_3i60n",
                       "display_name": "PrequelMemes",
                       "public_description": "Memes of the Star Wars Prequels",
                       "created_utc": "2016-12-27T03:05:47",
                       "subscribers": 1113167
                   }
               ],
               "bearer_token": "f8ba1f14f78b010aacc2a3c26abba5323445ba41"
           }
       }

-  **Error Response:**

-  **Code:** 400 Bad Request **Content:**

   .. code:: json

       {
           "error": {
               "code": 400,
               "messages": [
                   "detail: state param not found."
               ]
           }
       }

   OR

-  **Code:** 403 Forbidden **Content:**

   .. code:: json

       {
           "error": {
               "code": 403,
               "messages": [
                   "detail: Invalid or expired state."
               ]
           }
       }

-  **Notes:**

   The bearer token returned in success response json must be saved to
   use as the bearer token for all requests that need Authorization

Client details
--------------

Retrieves authenticated Reddit account info. GET request returns the
redditor data. Expects a valid bearer token in the Authorization header.

-  **URL**

   ``/clients/me``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/clients/me \
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
                       "id": "2qh0y",
                       "name": "t5_2qh0y",
                       "display_name": "Python",
                       "public_description": "news about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
                       "created_utc": "2008-01-25T03:14:39",
                       "subscribers": 462396
                   },
                   {
                       "id": "2r7yd",
                       "name": "t5_2r7yd",
                       "display_name": "learnprogramming",
                       "public_description": "A subreddit for all questions related to programming in any language.",
                       "created_utc": "2009-09-24T04:25:37",
                       "subscribers": 1179040
                   },
                   {
                       "id": "3i60n",
                       "name": "t5_3i60n",
                       "display_name": "PrequelMemes",
                       "public_description": "Memes of the Star Wars Prequels",
                       "created_utc": "2016-12-27T03:05:47",
                       "subscribers": 1113169
                   }
               ]
           }
       }

-  **Error Response:**

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

Client disconnect
-----------------

Disconnect a Salesforce Org Client. DELETE request that revokes Reddit access token,
deletes oauth token and changes the Client Org to inactive status. Expects a valid
bearer token in the Authorization header.

-  **URL**

   ``/clients/me``

-  **Method:**

   ``DELETE``

-  **Sample Call:**

   .. code:: shell

       http DELETE https://reddit-rest-api.herokuapp.com/clients/me \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "detail": "Account disconnected succesfully."
           }
       }

-  **Error Response:**

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

Salesforce Oauth
----------------

Initiates a Salesforce org OAuth using the connected app credentials and
returning the authorization URL.

-  **URL**

   ``/clients/salesforce_oauth``

-  **Method:**

   ``GET``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/clients/salesforce_oauth \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 **Content:**

   .. code:: json

       {
           "data": {
               "oauth_url": "https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9_XwsqeYoueKQ6jRFoG0mczO3WYS7B2N7bvuiZuhLJxHiBAyiFrF8zAA8yBTbDV9I4IwPGltSwnE3O087&prompt=consent&redirect_uri=https%3A%2F%2Freddit-rest-api.herokuapp.com%2Fclients%2Fsalesforce_oauth_callback&scope=full+refresh_token&state=41711",
               "state": "41711"
           }
       }

Salesforce Oauth Callback
-------------------------

Handles the callback from the Salesforce Oauth flow. Only used when the
user 'allows' or 'declines' the conditions in the Salesforce
authorization page.

-  **URL**

   ``/clients/salesforce_oauth_callback``

-  **Method:**

   ``GET``

-  **URL Params**

   **Required:**

   ``state=[integer]`` ``code=[string]``

   **Optional:**

   ``error=[integer]`` ``error_description=[string]``

-  **Sample Call:**

   .. code:: shell

       http GET https://reddit-rest-api.herokuapp.com/clients/salesforce_oauth_callback?state=11562&code=123456789

-  **Success Response:**

-  **Code:** 302 **Content:**

   Redirect to the Salesforce org instance that initiated the OAuth.

-  **Error Response:**

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/salesforce_oauth_callback``
   **Code:** 400 Bad Request **Content:**

   .. code:: json

       {
           "error": {
               "code": 400,
               "messages": [
                   "detail: state param not found."
               ]
           }
       }

   OR

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/salesforce_oauth_callback?state=abc``
   **Code:** 412 Precondition Failed **Content:**

   .. code:: json

       {
           "error": {
               "code": 412,
               "messages": [
                   "detail: Invalid or expired state."
               ]
           }
       }

   OR

-  **Call:**
   ``http GET https://reddit-rest-api.herokuapp.com/clients/salesforce_oauth_callback?error=access_denied&error_description=end-user+denied+authorization&state=52642``
   **Code:** 417 Expectation Failed **Content:**

   .. code:: json

       {
           "error": {
               "code": 417,
               "messages": [
                   "detail: end-user+denied+authorization"
               ]
           }
       }

Salesforce save token
---------------------

Recieves an access token and instance url of a Salesforce org to connect
this app with the org from the url. The access token is the one
generated with sfdx.

-  **URL**

   ``/clients/salesforce_token``

-  **Method:**

   ``POST``

-  **Data Params**

   **Required:**

   ``instance_url=[string]`` ``access_token=[string]``

   e.g:

   .. code:: json

       {
           "instance_url": "https://connect-page-7136-dev-ed.cs90.my.salesforce.com",
           "access_token": "1234567890.ABCDEFGH",
       }

-  **Sample Call:**

   .. code:: shell

       http POST https://reddit-rest-api.herokuapp.com/clients/salesforce_token \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
       instance_url=https://connect-page-7136-dev-ed.cs90.my.salesforce.com \
       access_token=1234567890.ABCDEFGH

-  **Success Response:**

-  **Code:** 201 Created **Content:**

   .. code:: json

       {
           "data": {
               "detail": "Salesforce org access token and instance url updated succesfully."
           }
       }

-  **Error Response:**

-  **Code:** 404 Not Found **Content:**

   .. code:: json

       {
           "data": {
               "status": "error",
               "detail": "Salesforce org with id: 123456789 not found in database."
           }
       }

   OR

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

Salesforce revoke token
-----------------------

Revokes the oauth access token for a Salesforce org according to the
Authorization bearer token.

-  **URL**

   ``/clients/salesforce_token``

-  **Method:**

   ``DELETE``

-  **Sample Call:**

   .. code:: shell

       http DELETE https://reddit-rest-api.herokuapp.com/clients/salesforce_token \
       'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'

-  **Success Response:**

-  **Code:** 200 OK **Content:**

   .. code:: json

       {
           "data": {
               "detail": "Oauth access token revoked for Salesforce org with id: 123456789.",
               "revoke_result": "Oauth token revoked successfully."
           }
       }

-  **Error Response:**

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
