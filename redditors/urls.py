from django.urls import path
import redditors.views as views

app_name = 'redditors'

urlpatterns = [
    path('', views.RedditorsInfo.as_view(), name='all_redditors'),
    path('<str:name>', views.RedditorInfo.as_view(), name='redditor_info'),
]
