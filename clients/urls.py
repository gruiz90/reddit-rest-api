from django.urls import path
import clients.views as views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientsView.as_view()),
    path('oauth', views.ClientOauthView.as_view(), name='oauth'),
    path(
        'oauth_callback', views.ClientOauthCallbackView.as_view(), name='oauth_callback'
    ),
    path(
        'oauth_confirm',
        views.ClientOauthConfirmationView.as_view(),
        name='oauth_confirm',
    ),
    path('disconnect', views.ClientDisconnectView.as_view(), name='disconnect'),
    path('me', views.ClientView.as_view(), name='me'),
    path(
        'salesforce_oauth', views.SalesforceOauthView.as_view(), name='salesforce_oauth'
    ),
    path(
        'salesforce_oauth_callback',
        views.SalesforceOauthCallbackView.as_view(),
        name='salesforce_oauth_callback',
    ),
    path(
        'salesforce_token', views.SalesforceTokenView.as_view(), name='salesforce_token'
    ),
    path(
        'salesforce_token_revoke',
        views.SalesforceRevokeAccessView.as_view(),
        name='salesforce_token_revoke',
    ),
]
