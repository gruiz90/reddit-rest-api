# Heroku Reddit API

[![Heroku](https://heroku-badge.herokuapp.com/?app=reddit-rest-api&root=clients/me)](https://reddit-rest-api.herokuapp.com)
[![Heroku CI Status](https://ci-badge.herokuapp.com/last.svg)](https://dashboard.heroku.com/pipelines/69207ad6-ac91-45c4-b653-4c464ba19bdb/tests)

A Heroku web app that provides a complete REST API with everything that the Salesforce org client needs to interact with Reddit.
(Authorization, subscriptions to subreddits, get submissions and comments from subreddits, create submissions and comments, reply to comments, upvote/downvote, direct messages to reddit users, ...)

## Important paths

* [Authorization](/clients)
* [Redditors](/redditors)
* [Subreddits](/subreddits)
* [Submissions](/submissions)
* [Comments](/comments)

REST API implemented using __DRF__ ([Django Rest Framework](https://github.com/encode/django-rest-framework)) and __PRAW__ ([Python Reddit API Wrapper](https://github.com/praw-dev/praw)).

<p align="center">
    <a href="https://www.django-rest-framework.org/" target="_blank">
        <img src="img_drf.png" />
    </a>
    <a href="https://praw.readthedocs.io/en/latest/index.html" target="_blank">
        <img src="img_praw.png"/>
    </a>
</p>
