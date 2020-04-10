Reddit REST API
===============

|Heroku| |Code Style|

.. |Heroku| image:: https://ci-badge.herokuapp.com/appdeployed?app=reddit-rest-api&root=clients/me
   :target: https://reddit-rest-api.herokuapp.com
.. |Code Style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

A Django web app that provides a REST API (kind of) with everything that
the Salesforce org client (or other clients, not necessarily Salesforce focused) needs to interact with Reddit.

Authorization, subscriptions to subreddits, get submissions and comments from
subreddits, create submissions and comments, reply to comments,
upvote/downvote and others.

Root paths
----------

-  `Clients and Authorization </clients>`__
-  `Subreddits </subreddits>`__
-  `Submissions </submissions>`__
-  `Comments </comments>`__
-  `Redditors </redditors>`__

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


Running the app locally:
------------------------

Required:
^^^^^^^^^

1. Python 3.8.X+ (`Python downloads <https://www.python.org/downloads/>`__)
2. Postgres 11+ (`Postgresql downloads <https://www.postgresql.org/download/>`__)
3. Redis 5+ (`Redis downloads <https://redis.io/download>`__)

Check the versions installed for each of the requirements:

    .. code:: shell

        $ python3 --version
            Python 3.8.2
        $ postgres --version
            postgres (PostgreSQL) 11.6
        $ redis-cli --version
            redis-cli 5.0.7

Environment variables:
^^^^^^^^^^^^^^^^^^^^^^

The API needs environment variables loaded in the PATH to work properly.
This variables can be added manually using the export command but the preferred way is to use a .env file.
This file needs to be added into the root of the folder, then when running the app Django automatically adds the environment variables with the correspondent values.


        DEBUG=True # Django Debug setting, True for development False for production recommended.

        DOMAIN_URL="http://localhost:8000" # This is for running locally (port 8000, 5000 if using heroku local), if running in a server then use the server domain URL.

        SECRET_KEY="*********************************" # Django secret key

    *For this variable the key needs to be generated*

        FIELD_ENCRYPTION_KEY="*********" # Check `<https://pypi.org/project/django-encrypted-model-fields/>`__ on how to do it.

        POSTGRES_USER="postgres" # Postgres username

        POSTGRES_DATABASE_NAME="django_reddit_api" # Postgres database name

        REDDIT_CLIENT_ID="******************" # Reddit API client id. Check `PRAW quickstart <https://praw.readthedocs.io/en/latest/getting_started/quick_start.html>`__

        REDDIT_CLIENT_SECRET="******************" # Reddit API secret

        REDDIT_USER_AGENT="test:reddit-rest-api:v1.0.0 (by /u/******)" # Reddit API user agent

        REDIS_URL="redis://127.0.0.1:6379/0" # Redis db URL

    *Only used with Salesforce oauth endpoints, not really mandatory*

        CONNECTED_APP_KEY="******************" # Salesforce connected app key

        CONNECTED_APP_SECRET="******************" # Salesforce connected app secret

Steps to create a virtual environment:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. After cloning the repository create the virual environment and activate it:

    .. code:: shell

        $ python3 -m venv venv
        $ source venv/bin/activate

2. Install requirements with pip:

    ``$ pip install -r requirements.txt``

3. Make migrations (Not really necessary) and migrate:

    .. code:: shell

        $ python manage.py makemigrations
        $ python manage.py migrate

4. Verify everything is working by executing tests:

        ``$ python manage.py test``

    *Message if all tests executed ok:*

        ::

            ----------------------------------------------------------------------
            Ran 23 tests in 100.914s

            OK
            Destroying test database for alias 'default'...

    **Tips to solve issues in this step:**

    - Check Postgres server is up and running.
    - Check Redis server ir up and running.
    - Check python and pip versions used in the vevn (virtual environment).
    - Check pip list command for the packages that are required are correcly installed.
    - Check environment variables are correctly set in .evn file.

5. Finally run locally the app:

    *Using python directly (Good way to test locally, but it's single-threaded)*

        .. code:: shell

            $ python manage.py runserver
            Watching for file changes with StatReloader
            Performing system checks...

            System check identified no issues (0 silenced).
            April 02, 2020 - 23:45:46
            Django version 2.2.6, using settings 'api.settings'
            Starting development server at http://127.0.0.1:8000/
            Quit the server with CONTROL-C.

    *Using heroku local command (This way the server is executed with gunicorn so it's multi-threaded)*

        .. code:: shell

            $ heroku local
            [OKAY] Loaded ENV .env File as KEY=VALUE Format
            8:46:44 PM web.1 |  [2020-04-02 20:46:44 -0300] [91987] [INFO] Starting gunicorn 19.9.0
            8:46:44 PM web.1 |  [2020-04-02 20:46:44 -0300] [91987] [INFO] Listening at: http://0.0.0.0:5000 (91987)
            8:46:44 PM web.1 |  [2020-04-02 20:46:44 -0300] [91987] [INFO] Using worker: sync
            8:46:45 PM web.1 |  /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/os.py:1023: RuntimeWarning: line buffering (buffering=1) isn't supported in binary mode, the default buffer size will be used
            8:46:45 PM web.1 |    return io.open(fd, *args, **kwargs)
            8:46:45 PM web.1 |  [2020-04-02 20:46:45 -0300] [91989] [INFO] Booting worker with pid: 91989

How to deploy app to Heroku and others
--------------------------------------

To deploy the app to heroku just push the code to the remote heroku master branch by using Heroku cli. Of course to be able to do this you need to add the remote of your heroku app.

Check this `Heroku deployment guide <https://devcenter.heroku.com/articles/git>`__ for details.

TODO: Using Docker would be cool as well `Docker! <https://www.docker.com/>`__.

Common Error Responses:
-----------------------

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

        {
            "error": {
                "code": 401,
                "messages": [
                    "detail: Invalid token."
                ]
            }
        }

        {
            "error": {
                "code": 401,
                "messages": [
                    "detail: Reddit access token authorization problem. The user may need to re-authorize the app. Exception raised: ResponseException('received 400 HTTP response')."
                ]
            }
        }
