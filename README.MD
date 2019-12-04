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

## Subreddits

All the endpoints provided to interact with Subreddits for an authorized client.

* [Subscriptions](#subreddits-subscriptions)
* [Subreddit Info](#subreddit-information)
* [Connect a Subreddit](#subreddit-connect)
* [Disconnect a Subreddit](#subreddit-disconnect)
* [Subscribe to a Subreddit](#subreddit-subscribe)
* [Unsubscribe to a Subreddit](#subreddit-unsubscribe)
* [Subreddit Rules](#subreddit-rules)

* **Common Error Responses for Subreddits endpoints:**

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

    OR

    * **Code:** 404 Not Found <br/>
    **Content:** <br/>

    ```json
    {
        "error": {
            "code": 404,
            "messages": [
                "detail: No subreddit exists with the name: notexistentsubredditname."
            ]
        }
    }
    ```

### Subreddits Subscriptions

Endpoint to get the list of subreddits subscriptions for the client.

* **URL**

    `/subreddits`

* **Method:**

    `GET`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/subreddits \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "subscriptions": [
                {
                    "id": "2qh0y",
                    "name": "t5_2qh0y",
                    "display_name": "Python",
                    "public_description": "news about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
                    "created_utc": "2008-01-25T03:14:39",
                    "subscribers": 462868
                },
                {
                    "id": "3i60n",
                    "name": "t5_3i60n",
                    "display_name": "PrequelMemes",
                    "public_description": "Memes of the Star Wars Prequels",
                    "created_utc": "2016-12-27T03:05:47",
                    "subscribers": 1114254
                }
            ]
        }
    }
    ```

### Subreddit Information

Endpoint to get the Subreddit data by the name provided in the URL.

* **URL**

    `/subreddits/<str:name>`

* **Method:**

    `GET`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/subreddits/python \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "id": "2qh0y",
            "name": "t5_2qh0y",
            "display_name": "Python",
            "description": "####[The Python Discord](https://discord.gg/python)\n\nNews about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python\n\n**If you are about to ask a \"how do I do this in python\" question, please try [r/learnpython](http://www.reddit.com/r/learnpython), [the Python discord](https://discord.gg/python), or the #python IRC channel on FreeNode.**\n\n**Please don't use URL shorteners**. Reddit filters them out, so your post or comment will be lost.\n\n**Posting code to this subreddit:**\n\nAdd 4 extra spaces before each line of code\n\n    def fibonacci():\n        a, b = 0, 1\n        while True:\n            yield a\n            a, b = b, a + b\n\n** ..........",
            "description_html": "<!-- SC_OFF --><div class=\"md\"><h4><a href=\"https://discord.gg/python\">The Python Discord</a></h4>\n\n<p>News about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python</p>\n\n<p><strong>If you are about to ask a &quot;how do I do this in python&quot; question, please try <a href=\"http://www.reddit.com/r/learnpython\">r/learnpython</a>, <a href=\"https://discord.gg/python\">the Python discord</a>, or the #python IRC channel on FreeNode.</strong></p>\n\n<p><strong>Please don&#39;t use URL shorteners</strong>. Reddit filters them out, ..........",
            "public_description": "news about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
            "created_utc": "2008-01-25T03:14:39",
            "subscribers": 462873,
            "spoilers_enabled": true,
            "over18": false,
            "can_assign_link_flair": false,
            "can_assign_user_flair": true
        }
    }
    ```

### Subreddit Connect

Endpoint that connects a Salesforce org client to a subreddit by the name. This creates a connection between the ClientOrg and the Subreddit models, subscribes the reddit user if not already and returns all the relevant data about the subreddit.

* **URL**

    `/subreddits/<str:name>/connect`

* **Method:**

    `POST`

* **Sample Call:**

    `http POST https://reddit-rest-api.herokuapp.com/subreddits/python/connect \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 201 Created <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "id": "2qh0y",
            "name": "t5_2qh0y",
            "display_name": "Python",
            "description": "####[The Python Discord](https://discord.gg/python)\n\nNews about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python\n\n**If you are about to ask a \"how do I do this in python\" question, please try [r/learnpython](http://www.reddit.com/r/learnpython), [the Python discord](https://discord.gg/python), or the #python IRC channel on FreeNode.**\n\n**Please don't use URL shorteners**. Reddit filters them out, so your post or comment will be lost.\n\n**Posting code to this subreddit:**\n\nAdd 4 extra spaces before each line of code\n\n    def fibonacci():\n        a, b = 0, 1\n        while True:\n            yield a\n            a, b = b, a + b\n\n** ..........",
            "description_html": "<!-- SC_OFF --><div class=\"md\"><h4><a href=\"https://discord.gg/python\">The Python Discord</a></h4>\n\n<p>News about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python</p>\n\n<p><strong>If you are about to ask a &quot;how do I do this in python&quot; question, please try <a href=\"http://www.reddit.com/r/learnpython\">r/learnpython</a>, <a href=\"https://discord.gg/python\">the Python discord</a>, or the #python IRC channel on FreeNode.</strong></p>\n\n<p><strong>Please don&#39;t use URL shorteners</strong>. Reddit filters them out, ..........",
            "public_description": "news about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
            "created_utc": "2008-01-25T03:14:39",
            "subscribers": 462873,
            "spoilers_enabled": true,
            "over18": false,
            "can_assign_link_flair": false,
            "can_assign_user_flair": true
        }
    }
    ```

### Subreddit Disconnect

Endpoint to disconnect a Salesforce org client to a Subreddit by the name. This only removes the connection between the ClientOrg and the Subreddit if exists.

* **URL**

    `/subreddits/<str:name>/disconnect`

* **Method:**

    `POST`

* **Sample Call:**

    `http POST https://reddit-rest-api.herokuapp.com/subreddits/python/disconnect \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Client disconnected subreddit succesfully."
        }
    }
    ```

### Subreddit Subscribe

Endpoint to subscribe a Salesforce org client to a subreddit by the name.

* **URL**

    `/subreddits/<str:name>/subscribe`

* **Method:**

    `POST`

* **Sample Call:**

    `http POST https://reddit-rest-api.herokuapp.com/subreddits/python/subscribe \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Client succesfully subscribed to python."
        }
    }
    ```

### Subreddit Unsubscribe

Endpoint to unsubscribe a Salesforce org client from a subreddit by the name.

* **URL**

    `/subreddits/<str:name>/unsubscribe`

* **Method:**

    `POST`

* **Sample Call:**

    `http POST https://reddit-rest-api.herokuapp.com/subreddits/python/unsubscribe \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Client succesfully unsubscribed from python."
        }
    }
    ```

### Subreddit Rules

Endpoint to get the rules of a subreddit by the name.

* **URL**

    `/subreddits/<str:name>/rules`

* **Method:**

    `GET`

* **Sample Call:**

    `http GET https://reddit-rest-api.herokuapp.com/subreddits/python/rules \`
    `'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'`

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "rules": [
                {
                    "kind": "link",
                    "description": "If you are about to ask a question about how to do something in python, please check out /r/learnpython. It is a very helpful community that is focused on helping people get answers that they understand.",
                    "short_name": "belongs in /r/learnpython",
                    "violation_reason": "belongs in /r/learnpython",
                    "created_utc": 1477520465.0,
                    "priority": 0,
                    "description_html": "<!-- SC_OFF --><div class=\"md\"><p>If you are about to ask a question about how to do something in python, please check out <a href=\"/r/learnpython\">/r/learnpython</a>. It is a very helpful community that is focused on helping people get answers that they understand.</p>\n</div><!-- SC_ON -->"
                },
                {
                    "kind": "link",
                    "description": "Please use other subreddits for things that are more generally programmer related, or for things that involve large snakes.",
                    "short_name": "not related to Python programming language",
                    "violation_reason": "not related to Python programming language",
                    "created_utc": 1477520552.0,
                    "priority": 1,
                    "description_html": "<!-- SC_OFF --><div class=\"md\"><p>Please use other subreddits for things that are more generally programmer related, or for things that involve large snakes.</p>\n</div><!-- SC_ON -->"
                }
            ],
            "site_rules": [
                "Spam",
                "Personal and confidential information",
                "Threatening, harassing, or inciting violence"
            ],
            "site_rules_flow": [
                {
                    "reasonTextToShow": "This is spam",
                    "reasonText": "This is spam"
                },
                {
                    "nextStepHeader": "In what way?",
                    "reasonTextToShow": "This is abusive or harassing",
                    "nextStepReasons": [
                        {
                            "nextStepHeader": "Who is the harassment targeted at?",
                            "reasonTextToShow": "It's targeted harassment",
                            "nextStepReasons": [
                                {
                                    "reasonTextToShow": "At me",
                                    "reasonText": "It's targeted harassment at me"
                                },
                                {
                                    "reasonTextToShow": "At someone else",
                                    "reasonText": "It's targeted harassment at someone else"
                                }
                            ],
                            "reasonText": ""
                        },
                        {
                            "nextStepHeader": "Who is the threat directed at?",
                            "reasonTextToShow": "It threatens violence or physical harm",
                            "nextStepReasons": [
                                {
                                    "reasonTextToShow": "At me",
                                    "reasonText": "It threatens violence or physical harm at me"
                                },
                                {
                                    "reasonTextToShow": "At someone else",
                                    "reasonText": "It threatens violence or physical harm at someone else"
                                }
                            ],
                            "reasonText": ""
                        },
                        {
                            "reasonTextToShow": "It's rude, vulgar or offensive",
                            "reasonText": "It's rude, vulgar or offensive"
                        },
                        {
                            "reasonTextToShow": "It's abusing the report button",
                            "canWriteNotes": true,
                            "isAbuseOfReportButton": true,
                            "notesInputTitle": "Additional information (optional)",
                            "reasonText": "It's abusing the report button"
                        }
                    ],
                    "reasonText": ""
                },
                {
                    "nextStepHeader": "What issue?",
                    "reasonTextToShow": "Other issues",
                    "nextStepReasons": [
                        {
                            "complaintButtonText": "File a complaint",
                            "complaintUrl": "https://www.reddit.com/api/report_redirect?thing=%25%28thing%29s&reason_code=COPYRIGHT",
                            "complaintPageTitle": "File a complaint?",
                            "reasonText": "It infringes my copyright",
                            "reasonTextToShow": "It infringes my copyright",
                            "fileComplaint": true,
                            "complaintPrompt": "If you think content on Reddit violates your intellectual property, please file a complaint at the link below:"
                        },
                        {
                            "complaintButtonText": "File a complaint",
                            "complaintUrl": "https://www.reddit.com/api/report_redirect?thing=%25%28thing%29s&reason_code=TRADEMARK",
                            "complaintPageTitle": "File a complaint?",
                            "reasonText": "It infringes my trademark rights",
                            "reasonTextToShow": "It infringes my trademark rights",
                            "fileComplaint": true,
                            "complaintPrompt": "If you think content on Reddit violates your intellectual property, please file a complaint at the link below:"
                        },
                        {
                            "reasonTextToShow": "It's personal and confidential information",
                            "reasonText": "It's personal and confidential information"
                        },
                        {
                            "reasonTextToShow": "It's sexual or suggestive content involving minors",
                            "reasonText": "It's sexual or suggestive content involving minors"
                        },
                        {
                            "nextStepHeader": "Do you appear in the image?",
                            "reasonTextToShow": "It's involuntary pornography",
                            "nextStepReasons": [
                                {
                                    "reasonTextToShow": "I appear in the image",
                                    "reasonText": "It's involuntary pornography and i appear in it"
                                },
                                {
                                    "reasonTextToShow": "I do not appear in the image",
                                    "reasonText": "It's involuntary pornography and i do not appear in it"
                                }
                            ],
                            "reasonText": ""
                        },
                        {
                            "reasonTextToShow": "It's a transaction for prohibited goods or services",
                            "reasonText": "It's a transaction for prohibited goods or services"
                        },
                        {
                            "complaintButtonText": "File a complaint",
                            "complaintUrl": "https://www.reddit.com/api/report_redirect?thing=%25%28thing%29s&reason_code=NETZDG",
                            "complaintPageTitle": "File a complaint?",
                            "reasonText": "Report this content under NetzDG",
                            "reasonTextToShow": "Report this content under NetzDG",
                            "fileComplaint": true,
                            "complaintPrompt": "This reporting procedure is only available for people in Germany. If you are in Germany and would like to report this content under the German Netzwerkdurchsetzungsgesetz (NetzDG) law you may file a complaint by clicking the link below."
                        },
                        {
                            "complaintButtonText": "Visit Help Center",
                            "complaintUrl": "https://www.reddit.com/api/report_redirect?thing=%25%28thing%29s&reason_code=SELF_HARM",
                            "complaintPageTitle": "Reporting and responding to people considering suicide or serious self-harm",
                            "reasonText": "Someone is considering suicide or serious self-harm",
                            "reasonTextToShow": "Someone is considering suicide or serious self-harm",
                            "fileComplaint": true,
                            "complaintPrompt": "If someone is considering suicide, showing kindness and understanding can go a long way. If they're inside the U.S., let them know that you care and encourage them to text \"CHAT\" to 741741. They'll be connected to a trained Crisis Counselor from Crisis Text Line. For more information, including resources available for people outside the U.S., visit our help center."
                        }
                    ],
                    "reasonText": ""
                }
            ]
        }
    }
    ```