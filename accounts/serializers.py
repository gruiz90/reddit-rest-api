from rest_framework import serializers
from .models import SalesforceOrg, ClientOrg
from redditors.serializers import RedditorSerializer
from redditors.models import Redditor


class ClientOrgSerializer(serializers.ModelSerializer):
    redditor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClientOrg
        # fields = ['redditor', 'salesforce_org',
        #           'timestamp_client_connected',
        #           'timestamp_client_disconnected',
        #           'last_time_client_request',
        #           'last_time_client_updated', ]
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return ClientOrg.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp_client_connected = validated_data.get(
            'timestamp_client_connected', instance.timestamp_client_connected)
        instance.timestamp_client_disconnected = validated_data.get(
            'timestamp_client_disconnected', instance.timestamp_client_disconnected)
        instance.last_time_client_request = validated_data.get(
            'last_time_client_request', instance.last_time_client_request)
        instance.last_time_client_updated = validated_data.get(
            'last_time_client_updated', instance.last_time_client_updated)
        instance.reddit_token = validated_data.get(
            'reddit_token', instance.reddit_token)
        instance.client_token = validated_data.get(
            'client_token', instance.client_token)
        instance.save()
        return instance

    # def create(self, validated_data):
    #     salesforce_org = validated_data.pop('salesforce_org')
    #     redditor = validated_data.pop('redditor')
    #     return ClientOrg.objects.create(redditor=redditor, salesforce_org=salesforce_org, **validated_data)


class SalesforceOrgSerializer(serializers.ModelSerializer):
    clients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SalesforceOrg
        fields = ['org_id', 'org_name', 'org_url',
                  'package_version', 'clients', ]
        read_only = ['org_id']
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

    # def create(self, validated_data):
    #     clients_data = validated_data.pop('clients')
    #     salesforce_org = SalesforceOrg.objects.create(**validated_data)
    #     for client_data in clients_data:
    #         ClientOrg.objects.create(
    #             salesforce_org=salesforce_org, **client_data)
    #     return salesforce_org


# class SalesforceOrgSerializer(serializers.ModelSerializer):
#     clients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = SalesforceOrg
#         fields = ['org_id', 'org_name', 'org_url',
#                   'package_version', 'clients', ]
#         depth = 1


# class ClientOrgSerializer(serializers.ModelSerializer):
#     salesforce_org_id = serializers.PrimaryKeyRelatedField(
#         source='salesforce_org', read_only=True
#     )
#     salesforce_org = SalesforceOrgSerializer(read_only=True)
#     redditor_id = serializers.PrimaryKeyRelatedField(
#         source='redditor', read_only=True
#     )
#     redditor = RedditorSerializer(read_only=True)

#     class Meta:
#         model = ClientOrg
#         fields = ['timestamp_client_connected',
#                   'timestamp_client_disconnected',
#                   'last_time_client_request',
#                   'last_time_client_updated',
#                   'salesforce_org', 'salesforce_org_id',
#                   'redditor', 'redditor_id', ]
#         depth = 1

    # def create(self, validated_data):
    #     org_data = validated_data.pop('org_data')

    #     org_clients_data = validated_data.pop('org_clients')
    #     org_data = OrgData.objects.create(**validated_data)
    #     for org_client_data in org_clients_data:
    #         OrgClient.objects.create(org_data=org_data, **org_client_data)
    #     return org_data
    #     pass
