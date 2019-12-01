from rest_framework import serializers
from .models import SalesforceOrg, ClientOrg
from redditors.models import Redditor
from redditors.serializers import RedditorSerializer


class ClientOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOrg
        # fields = ['redditor', 'salesforce_org',
        #           'connected_at',
        #           'disconnected_at',
        #           'last_client_request_at',
        #           'last_client_update_at', ]
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return ClientOrg.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.connected_at = validated_data.get(
            'connected_at', instance.connected_at)
        instance.disconnected_at = validated_data.get(
            'disconnected_at', instance.disconnected_at)
        instance.last_client_request_at = validated_data.get(
            'last_client_request_at', instance.last_client_request_at)
        instance.last_client_update_at = validated_data.get(
            'last_client_update_at', instance.last_client_update_at)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.reddit_token = validated_data.get(
            'reddit_token', instance.reddit_token)
        instance.save()
        return instance


class SalesforceOrgSerializer(serializers.ModelSerializer):
    clients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SalesforceOrg
        fields = ['org_id', 'org_name', 'org_url',
                  'package_version', 'clients',
                  'created_at', 'updated_at']
        read_only = ['org_id', 'created_at', 'updated_at']
        depth = 1

    def create(self, validated_data):
        return SalesforceOrg.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.org_name = validated_data.get('org_name', instance.org_name)
        instance.org_url = validated_data.get('org_url', instance.org_url)
        instance.package_version = validated_data.get(
            'package_version', instance.package_version)
        instance.save()
        return instance
