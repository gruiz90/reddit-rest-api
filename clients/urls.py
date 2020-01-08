from django.urls import path
import clients.views as views

app_name = 'clients'

urlpatterns = [
	path('', views.ClientsView.as_view()),
    path('oauth', views.ClientOauthView.as_view()),
    path('oauth_callback', views.ClientOauthCallbackView.as_view()),
    path('oauth_confirm', views.ClientOauthConfirmationView.as_view()),
	path('me', views.ClientView.as_view()),
    path('disconnect', views.ClientDisconnectView.as_view()),
	path('salesforce_oauth/<str:org_id>', views.SalesforceOauthView.as_view()),
	path('salesforce_oauth_callback', views.SalesforceOauthCallbackView.as_view()),
]
