# Heroku Reddit API

A Heroku web app that provides a complete API with everything that the Salesforce org client needs to interact with Reddit.
(Authorization, subscriptions to subreddits, get submissions and comments from subreddits, create submissions and comments, reply to comments, upvote/downvote, direct messages to reddit users, ...)

Hosted in: https://reddit-rest-api.herokuapp.com/

## API important routes

* [Authorization](#clients-authorization)
* [Subreddits](#subreddits)
* [Redditors](#redditors)

## Clients Authorization

All the endpoints provided to authorize a Reddit account from a Salesforce organization.

* [Oauth Init](#client-oauth)
* [Oauth Callback](#client-oauth-callback)
* [Oauth Status](#client-check-oauth-status)
* [Oauth Confirm](#client-confirm-authorization)
* [View client details](#view-client-details)
* [Disconnect client](#disconnect-client)

### Client Oauth

Initiates the Reddit Account oauth flow.

* **URL**

    `/clients/oauth`

* **Method:**

    `GET`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/clients/oauth`

* **Success Response:**

  * **Code:** 200 <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "oauth_url": "https://www.reddit.com/api/v1/authorize?client_id=PJzoDgMB6HJUDA&duration=permanent&redirect_uri=https%3A%2F%2Freddit-rest-api.herokuapp.com%2Foauth_callback&response_type=code&scope=%2A&state=54221",
            "state": "54221"
        }
    }
    ```

### Client Oauth Callback

Handles the callback from the Reddit Oauth flow. Only used when the user 'allows' or 'declines' the conditions in the reddit authorization page.

* **URL**

    `/clients/oauth_callback`

* **Method:**

    `GET`

* **URL Params**

    **Required:**

    `state=[integer]`
    `code=[string]`

    **Optional:**

    `error=[integer]`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback?state=11562&code=_TvTWeuxQI8YQ_eZE-7bfbc0QmI`

* **Success Response:**

  * **Code:** 200 <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Oauth code saved successfully."
        }
    }
    ```

* **Error Response:**

  * **Call:** `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback` <br/>
    **Code:** 400 Bad Request <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 400,
            "messages": [
                "detail: state param not found."
            ]
        }
    }
    ```

    OR

  * **Call:** `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback?state=abc` <br/>
    **Code:** 403 Forbidden <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 403,
            "messages": [
                "detail: Invalid or expired state."
            ]
        }
    }
    ```

    OR

  * **Call:** `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_callback?state=11562&error=access_denied` <br/>
    **Code:** 403 Forbidden <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 403,
            "messages": [
                "detail: access_denied"
            ]
        }
    }
    ```

### Client check oauth status

Check oauth status for a Salesforce organization client.

* **URL**

    `/clients/oauth_confirm`

* **Method:**

    `GET`

* **URL Params**

    **Required:**

    `state=[integer]`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_confirm?state=11562`

* **Success Response:**

  * **Code:** 202 <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Authorization still pending."
        }
    }
    ```

    OR

    * **Code:** 200 <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "result": "accepted",
            "detail": "Authorization complete."
        }
    }
    ```

    OR

    * **Code:** 200 <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "result": "error",
            "detail": "access_denied"
        }
    }
    ```

* **Error Response:**

  * **Call:** `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_confirm` <br/>
    **Code:** 400 Bad Request <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 400,
            "messages": [
                "detail: state param not found."
            ]
        }
    }
    ```

    OR

  * **Call:** `http GET https://reddit-rest-api.herokuapp.com/clients/oauth_confirm?state=abc` <br/>
    **Code:** 403 Forbidden <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 403,
            "messages": [
                "detail: Invalid or expired state."
            ]
        }
    }
    ```

### Client Confirm Authorization

Handles the autorization confirmation of a Reddit account for a Salesforce organization

* **URL**

    `/clients/oauth_confirm`

* **Method:**

    `POST`

* **URL Params**

    **Required:**

    `state=[integer]`

* **Data Params**

    **Required:**

    `org_id=[string]`
    `org_name=[string]`
    `org_url=[string]`
    `org_name=[string]`

    **Optional:**
    `package_version=[string]`

    e.g:
    ```json
    {
        "org_id": "testorgid",
        "org_name": "test",
        "org_url": "http://test.com",
        "package_version":"1.0"
    }
    ```

* **Sample Call:**

    `http POST https://reddit-rest-api.herokuapp.com/clients/oauth_confirm?state=11562 \`
    `org_id=testorgid org_name=test org_url=http://test.com package_version=1.0`

* **Success Response:**

  * **Code:** 201 Created <br/>
    **Content:** <br/>

    ```json
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
    ```

* **Error Response:**

  * **Code:** 400 Bad Request <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 400,
            "messages": [
                "detail: state param not found."
            ]
        }
    }
    ```

    OR

  * **Code:** 403 Forbidden <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 403,
            "messages": [
                "detail: Invalid or expired state."
            ]
        }
    }
    ```

* **Notes:**

    The bearer token returned in success response json must be saved to use as the bearer token for all requests that need Authorization

### View Client details

Retrieves authenticated Reddit account info. GET request returns the redditor data.
Expects a valid bearer token in the Authorization header.

* **URL**

    `/clients/me`

* **Method:**

    `GET`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/clients/me \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
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
                    "display_name": "Python",
                    "public_description": "news about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
                    "subscribers": 462394
                },
                {
                    "id": "2r7yd",
                    "display_name": "learnprogramming",
                    "public_description": "A subreddit for all questions related to programming in any language.",
                    "subscribers": 1179033
                },
                {
                    "id": "3i60n",
                    "display_name": "PrequelMemes",
                    "public_description": "Memes of the Star Wars Prequels",
                    "subscribers": 1113169
                }
            ]
        }
    }
    ```

* **Error Response:**

  * **Code:** 401 Unauthorized <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 401,
            "messages": [
                "detail: Authentication credentials were not provided."
            ]
        }
    }
    ```

    OR

  * **Code:** 401 Unauthorized <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 401,
            "messages": [
                "detail: Invalid token."
            ]
        }
    }
    ```

### Disconnect Client

Disconnect a Salesforce Org Client. DELETE request that deletes oauth token and
changes the Client Org to inactive status.
Expects a valid bearer token in the Authorization header.

* **URL**

    `/clients/disconnect`

* **Method:**

    `DELETE`

* **Sample Call:**

    `http DELETE https://reddit-rest-api.herokuapp.com/clients/me \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Account disconnected succesfully."
        }
    }
    ```

* **Error Response:**

  * **Code:** 401 Unauthorized <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 401,
            "messages": [
                "detail: Authentication credentials were not provided."
            ]
        }
    }
    ```

    OR

  * **Code:** 401 Unauthorized <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 401,
            "messages": [
                "detail: Invalid token."
            ]
        }
    }
    ```