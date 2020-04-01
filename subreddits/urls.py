from django.urls import path
import subreddits.views as views

app_name = 'subreddits'

urlpatterns = [
    path('', views.SubredditSubscriptions.as_view(), name='subreddit_subscriptions'),
    path('<str:name>', views.Subreddit.as_view(), name='subreddit'),
    path(
        '<str:name>/connect', views.SubredditConnect.as_view(), name='subreddit_connect'
    ),
    path(
        '<str:name>/disconnect',
        views.SubredditDisconnect.as_view(),
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
        '<str:name>/submissions',
        views.SubredditSubmissions.as_view(),
        name='subreddit_submissions',
    ),
]
