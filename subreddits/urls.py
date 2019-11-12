from django.urls import path, include
from rest_framework import routers
from .views import SubredditViewSet

app_name = 'subreddits'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('subreddits', SubredditViewSet)

urlpatterns = router.urls