from django.urls import path
from .views import RedditorAccountView

app_name = 'redditors'

urlpatterns = [
    path('me', RedditorAccountView.as_view()),
]
