from django.urls import path
import clients.views as views

app_name = 'clients'

urlpatterns = [
	path('', views.ClientView.as_view()),
    path('oauth', views.ClientOauthView.as_view()),
    path('oauth_callback', views.ClientOauthCallbackView.as_view()),
    path('oauth_confirm', views.ClientOauthConfirmationView.as_view()),
    path('disconnect', views.ClientDisconnectView.as_view()),
]
