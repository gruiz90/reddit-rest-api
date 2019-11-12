from .models import Subreddit
from rest_framework import serializers, viewsets


class SubredditSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subreddit
        fields = ['id', 'url', 'name', 'display_name',
                  'description', 'public_description', 'created_utc', 'subscribers', 'over18']