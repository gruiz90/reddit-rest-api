Heroku Reddit API
=================

|Heroku| |Heroku CI Status| |Code Style|

.. |Heroku| image:: https://ci-badge.herokuapp.com/appdeployed?app=reddit-rest-api&root=clients/me
   :target: https://reddit-rest-api.herokuapp.com
.. |Heroku CI Status| image:: https://ci-badge.herokuapp.com/last.svg
   :target: https://dashboard.heroku.com/pipelines/69207ad6-ac91-45c4-b653-4c464ba19bdb/tests
.. |Code Style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

A Heroku web app that provides a complete REST API with everything that
the Salesforce org client needs to interact with Reddit. (Authorization,
subscriptions to subreddits, get submissions and comments from
subreddits, create submissions and comments, reply to comments,
upvote/downvote, direct messages to reddit users, ...)

Important paths
---------------

-  `Authorization </clients>`__
-  `Redditors </redditors>`__
-  `Subreddits </subreddits>`__
-  `Submissions </submissions>`__
-  `Comments </comments>`__

REST API implemented using **DRF** (`Django Rest Framework <https://github.com/encode/django-rest-framework>`__) and
**PRAW** (`Python Reddit APIWrapper <https://github.com/praw-dev/praw>`__).

.. raw:: html

    <p align="center">
        <a href="https://www.django-rest-framework.org/" target="_blank">
            <img src="img_drf.png" />
        </a>
        <a href="https://praw.readthedocs.io/en/latest/index.html" target="_blank">
            <img src="img_praw.png"/>
        </a>
    </p>


-  **Common errors:**

    .. code:: json

        {
            "error": {
                "code": 401,
                "messages": [
                    "detail: Reddit access token authorization problem. The user may need to re-authorize the app. Exception raised: ResponseException('received 400 HTTP response')."
                ]
            }
        }


