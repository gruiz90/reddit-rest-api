from .models import Subreddit
from rest_framework import serializers
from clients.serializers import ClientOrgSerializer


class SubredditSerializer(serializers.ModelSerializer):
    clients = ClientOrgSerializer(many=True, read_only=True)

    class Meta:
        model = Subreddit
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        return Subreddit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.display_name = validated_data.get(
            'display_name', instance.display_name
        )
        instance.description = validated_data.get('description', instance.description)
        instance.description_html = validated_data.get(
            'description_html', instance.description_html
        )
        instance.public_description = validated_data.get(
            'public_description', instance.public_description
        )
        instance.created_utc = validated_data.get('created_utc', instance.created_utc)
        instance.subscribers = validated_data.get('subscribers', instance.subscribers)
        instance.spoilers_enabled = validated_data.get(
            'spoilers_enabled', instance.spoilers_enabled
        )
        instance.over18 = validated_data.get('over18', instance.over18)
        instance.can_assign_link_flair = validated_data.get(
            'can_assign_link_flair', instance.can_assign_link_flair
        )
        instance.can_assign_user_flair = validated_data.get(
            'can_assign_user_flair', instance.can_assign_user_flair
        )
        instance.save()
        return instance
