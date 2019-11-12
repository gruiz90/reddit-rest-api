from django.urls import path
from .views import AccountOauthView

app_name = 'accounts'

urlpatterns = [
    path('', AccountOauthView.as_view()),
]
