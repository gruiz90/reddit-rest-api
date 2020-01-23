from django.urls import path
import redditors.views as views

app_name = 'redditors'

urlpatterns = [
    path('', views.RedditorAccountView.as_view(), name='my_redditor'),
	path('<str:name>', views.RedditorView.as_view(), name='redditor_info'),
]
