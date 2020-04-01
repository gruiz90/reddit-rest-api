from django.urls import path
import clients.views as views

app_name = 'clients'

urlpatterns = [
    # path('', views.ClientsInfo.as_view(), name='all_clients'),
    path('oauth', views.ClientOauth.as_view(), name='oauth'),
    path('oauth_callback', views.ClientOauthCallback.as_view(), name='oauth_callback'),
    path(
        'oauth_confirm', views.ClientOauthConfirmation.as_view(), name='oauth_confirm',
    ),
    path('me', views.Client.as_view(), name='me'),
    path('salesforce_oauth', views.SalesforceOauth.as_view(), name='salesforce_oauth'),
    path(
        'salesforce_oauth_callback',
        views.SalesforceOauthCallback.as_view(),
        name='salesforce_oauth_callback',
    ),
    path('salesforce_token', views.SalesforceToken.as_view(), name='salesforce_token'),
]
