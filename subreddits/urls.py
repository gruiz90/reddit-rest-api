from django.urls import path
import subreddits.views as views

app_name = 'subreddits'

urlpatterns = [
    path('', views.SubredditSubscriptions.as_view(), name='subreddit_subscriptions'),
    path('<str:name>', views.SubredditInfo.as_view(), name='subreddit_info'),
    path(
        '<str:name>/connect', views.ConnectSubreddit.as_view(), name='subreddit_connect'
    ),
    path(
        '<str:name>/disconnect',
        views.DisconnectSubreddit.as_view(),
        name='subreddit_disconnect',
    ),
    path('<str:name>/rules', views.SubredditRules.as_view(), name='subreddit_rules'),
    path(
        '<str:name>/subscribe',
        views.SubredditSubscribe.as_view(),
        name='subreddit_subscribe',
    ),
    path(
        '<str:name>/unsubscribe',
        views.SubredditUnsubscribe.as_view(),
        name='subreddit_unsubscribe',
    ),
    path(
        '<str:name>/submit',
        views.SubredditSubmitSubmission.as_view(),
        name='subreddit_submit_submission',
    ),
    path(
        '<str:name>/submissions',
        views.SubredditSubmissions.as_view(),
        name='subreddit_submissions',
    ),
]
