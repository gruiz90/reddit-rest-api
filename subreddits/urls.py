from django.urls import path
import subreddits.views as views

app_name = 'subreddits'

urlpatterns = [
    # path('', views.SubredditsDetails.as_view(), name='subreddits_details'),
    path(
        'subscriptions',
        views.SubredditsSubscriptions.as_view(),
        name='subscriptions',
    ),
    path('<str:name>', views.SubredditDetails.as_view(), name='subreddit'),
    path(
        '<str:name>/connections', views.SubredditConnections.as_view(), name='subreddit_connections'
    ),
    path('<str:name>/rules', views.SubredditRules.as_view(), name='subreddit_rules'),
    path(
        '<str:name>/submissions',
        views.SubredditSubmissions.as_view(),
        name='subreddit_submissions',
    ),
]
