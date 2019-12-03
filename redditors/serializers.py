from rest_framework import serializers
from .models import Redditor


class RedditorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Redditor
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        return Redditor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.has_verified_email = validated_data.get(
            'has_verified_email', instance.has_verified_email)
        instance.icon_img = validated_data.get('icon_img', instance.icon_img)
        instance.comment_karma = validated_data.get(
            'comment_karma', instance.comment_karma)
        instance.link_karma = validated_data.get(
            'link_karma', instance.link_karma)
        instance.num_friends = validated_data.get(
            'num_friends', instance.num_friends)
        instance.is_employee = validated_data.get(
            'is_employee', instance.is_employee)
        instance.is_friend = validated_data.get(
            'is_friend', instance.is_friend)
        instance.is_mod = validated_data.get('is_mod', instance.is_mod)
        instance.is_gold = validated_data.get('is_gold', instance.is_gold)
        instance.save()
        return instance
