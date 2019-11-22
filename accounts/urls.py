from django.urls import path
from .views import AccountOauthView, AccountOauthCallbackView, AccountOauthConfirmationView

app_name = 'accounts'

urlpatterns = [
    path('oauth', AccountOauthView.as_view()),
    path('oauth_callback', AccountOauthCallbackView.as_view()),
    path('oauth_confirm', AccountOauthConfirmationView.as_view()),
    # path('oauth_confirm', AccountOauthConfirmationView.as_view()),
]
