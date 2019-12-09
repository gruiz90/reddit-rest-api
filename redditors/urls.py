from django.urls import path
import redditors.views as views

app_name = 'redditors'

urlpatterns = [
    path('', views.RedditorAccountView.as_view()),
	path('<str:name>', views.RedditorView.as_view()),
]
