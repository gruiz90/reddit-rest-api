# Heroku Reddit API

A Heroku web app that provides a complete API with everything that the Salesforce org client needs to interact with Reddit.
(Authorization, subscriptions to subreddits, get submissions and comments from subreddits, create submissions and comments, reply to comments, upvote/downvote, direct messages to reddit users, ...)

Hosted in: https://reddit-rest-api.herokuapp.com/

## API important routes

* [Authorization](/clients)
* [Redditors](#redditors)
* [Subreddits](#subreddits)
* [Submissions](#submissions)
* [Comments](#comments)


## Redditors

All the endpoints provided to interact with Redditors for an authorized client.

* [My Redditor Information](#my-redditor-data)
* [Redditor Info](#get-redditor-data)

### Common Error Responses for Redditors endpoints:

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
                "detail: No redditor exists with the name: ???."
            ]
        }
    }
    ```

### My Redditor Data

Endpoint to get the authorized reddit account redditor data and subscriptions.

* **URL**

    `/redditors`

* **Method:**

    `GET`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/redditors/sfdctest \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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
    ```

### Get Redditor Data

Endpoint to get the Redditor data by the name provided in the URL.

* **URL**

    `/redditors/<str:name>`

* **Method:**

    `GET`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/redditors/sfdctest \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
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
* [Subreddit Submissions](#subreddit-submissions)

### Common Error Responses for Subreddits endpoints:

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
                "detail: No subreddit exists with the name: ???."
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

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/subreddits \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/subreddits/python \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

    ```shell
    http POST https://reddit-rest-api.herokuapp.com/subreddits/python/connect \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

    ```shell
    http POST https://reddit-rest-api.herokuapp.com/subreddits/python/disconnect \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

    ```shell
    http POST https://reddit-rest-api.herokuapp.com/subreddits/python/subscribe \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

    ```shell
    http POST https://reddit-rest-api.herokuapp.com/subreddits/python/unsubscribe \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/subreddits/python/rules \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

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

### Subreddit Submissions

Endpoint to get a Subreddit's Submissions. It returns a max of 5 submissions per request. Need to use an offset to get the rest in different requests. Param time_filter only used when sort=[controversial|top].

* **URL**

    `/subreddits/<str:name>/submissions`

* **Method:**

    `GET`

* **URL Params**

    **Optional:**

    `sort=[hot|controversial|gilded|new|rising|top] (default=hot)`
    `time_filter=[all|day|hour|month|week|year] (default=all)`
    `offset=[0<=int] (default=0)`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/subreddits/python/submissions?sort=top&time_filter=month&limit=3 \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "submissions": [
                {
                    "id": "e2234a",
                    "name": "t3_e2234a",
                    "title": "hashtags",
                    "created_utc": "2019-11-26T18:26:29",
                    "author_name": "Williamismijnnaam",
                    "num_comments": 120,
                    "score": 2830,
                    "url": "https://i.redd.it/8ss44ve160141.jpg"
                },
                {
                    "id": "dz81ed",
                    "name": "t3_dz81ed",
                    "title": "My 12 year old just shouted \"Dad I made a copy of flappy birds\". My response \"Yeah right!\". To my amazement he did. I genuinely didn't even know he was doing this. He used Python and PyGame apparently.",
                    "created_utc": "2019-11-20T20:47:51",
                    "author_name": "doggertron_",
                    "num_comments": 202,
                    "score": 2501,
                    "url": "https://i.redd.it/7sb9ffimlwz31.png"
                },
                {
                    "id": "dvw09b",
                    "name": "t3_dvw09b",
                    "title": "BrachioGraph, an ultra-cheap Python-powered drawing machine",
                    "created_utc": "2019-11-13T18:34:37",
                    "author_name": "EvilDMP",
                    "num_comments": 59,
                    "score": 2149,
                    "url": "https://v.redd.it/w4f0q6tbzhy31"
                },
                {
                    "id": "e1ldoz",
                    "name": "t3_e1ldoz",
                    "title": "A fitting curve that \"boings\" into place (and a digression into spring-mass-dampers, vibration and control theory, and integral transforms)",
                    "created_utc": "2019-11-25T19:41:33",
                    "author_name": "Chemomechanics",
                    "num_comments": 55,
                    "score": 2116,
                    "url": "https://i.redd.it/tp80yhyrwv041.gif"
                },
                {
                    "id": "dxq4ea",
                    "name": "t3_dxq4ea",
                    "title": "This is one of the most interesting outputs of the particle simulation :)",
                    "created_utc": "2019-11-17T18:16:00",
                    "author_name": "chrismit3s",
                    "num_comments": 125,
                    "score": 1962,
                    "url": "https://v.redd.it/ib5nkw7ifaz31"
                }
            ],
            "sort": "top",
            "time_filter": "month",
            "offset": 0
        }
    }
    ```

## Submissions

All the endpoints provided to interact with Submissions for an authorized client.

* [Submission Information](#submission-information)
* [Submission Comments](#submission-comments)
* [Submission Post Vote](#submission-vote)

### Common Error Responses for Submissions endpoints:

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
                "detail: No submission exists with the id: ???."
            ]
        }
    }
    ```

### Submission Information

Endpoint to get the Submission data by the id provided in the URL.

* **URL**

    `/submissions/<str:id>`

* **Method:**

    `GET`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/submissions/e8ge80 \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
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
    ```

### Submission Comments

Endpoint to get a Submission's comments. It returns a max of 20 comments per request. Uses offset to get the rest in different requests. The flat parameter is used to retrieve comments with lower level than top level. The order of the list with flat=True is [Comments_Level1, Comments_Level2, ..., Comments_LevelN]

* **URL**

    `/submissions/<str:id>/comments`

* **Method:**

    `GET`

* **URL Params**

    **Optional:**

    `sort=[best|top|new|controversial|old|q&a] (default=best)`
    `limit=[0<int<21] (default=10)`
    `offset=[0<=int] (default=0)`
    `flat=[True|False] (default=False)`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/submissions/e7t00m/comments?sort=top&limit=2&offset=3 \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
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
            "sort": "top",
            "limit": 2,
            "offset": 3,
            "flat": false
        }
    }
    ```

### Submission Vote

Endpoint to post a vote for a submission by the id provided in the url. Passing vote_value = [-1|0|1] a downvote, clear_vote, upvote action is executed for the submission.

* **URL**

    `/submissions/<str:id>/vote`

* **Method:**

    `POST`

* **Data Params**

    **Required:**

    `vote_value=[-1<=int<=1]`

    e.g:

    ```json
    {
        "vote_value": 1
    }
    ```

* **Sample Call:**

    ```shell
    http POST https://reddit-rest-api.herokuapp.com/submissions/e8a0c7/vote \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
    vote_value=1
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Vote action 'Upvote' successful for submission with id: e8a0c7!"
        }
    }
    ```

## Comments

All the endpoints provided to interact with Comments for an authorized client.

* [Comment Information](#comment-information)
* [Comment Replies](#comment-replies)
* [Comment Post Vote](#comment-vote)

### Common Error Responses for Comments endpoints:

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
                "detail: No comment exists with the id: ???."
            ]
        }
    }
    ```

### Comment Information

Endpoint to get the Comment data by the id provided in the URL.

* **URL**

    `/comments/<str:id>`

* **Method:**

    `GET`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/comments/faab0e4 \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
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
    ```

### Comment Replies

Endpoint to get a Comment's replies. It returns a max of 20 replies per request. Uses offset to get the rest in different requests. The flat parameter is used to retrieve replies with lower level than top level. The order of the list with flat=True is [Reply_Level1, Reply_Level2, ..., Reply_LevelN]

* **URL**

    `/comments/<str:id>/replies`

* **Method:**

    `GET`

* **URL Params**

    **Optional:**

    `limit=[0<int<21] (default=10)`
    `offset=[0<=int] (default=0)`
    `flat=[True|False] (default=False)`

* **Sample Call:**

    ```shell
    http GET https://reddit-rest-api.herokuapp.com/comments/faab0e4/replies?limit=2&flat=True \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa'
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
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
            "limit": 2,
            "offset": 0,
            "flat": "True"
        }
    }
    ```

### Comment Vote

Endpoint to post a vote for a comment by the id provided in the url. Passing vote_value = [-1|0|1] a downvote, clear_vote, upvote action is executed for the submission.

* **URL**

    `/comment/<str:id>/vote`

* **Method:**

    `POST`

* **Data Params**

    **Required:**

    `vote_value=[-1<=int<=1]`

    e.g:

    ```json
    {
        "vote_value": 1
    }
    ```

* **Sample Call:**

    ```shell
    http POST https://reddit-rest-api.herokuapp.com/comment/faab0e4/vote \
    'Authorization:Bearer 30ad9388f15b1da7ef6c08b03721a1f08b5426fa' \
    vote_value=1
    ```

* **Success Response:**

  * **Code:** 200 OK <br/>
    **Content:** <br/>

    ```json
    {
        "data": {
            "detail": "Vote action 'Upvote' successful for submission with id: e8a0c7!"
        }
    }
    ```