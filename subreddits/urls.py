from django.urls import path
import subreddits.views as views

app_name = 'subreddits'

urlpatterns = [
	path('', views.SubredditSubscriptions.as_view()),
	path('<str:name>', views.SubredditView.as_view()),
	path('<str:name>/connect', views.ConnectSubreddit.as_view()),
	path('<str:name>/disconnect', views.DisconnectSubreddit.as_view()),
	path('<str:name>/rules', views.SubredditRules.as_view()),
	path('<str:name>/subscribe', views.SubredditSubscribe.as_view()),
	path('<str:name>/unsubscribe', views.SubredditUnsubscribe.as_view()),
]
