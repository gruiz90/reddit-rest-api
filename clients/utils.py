#!/usr/bin/env python3
from django.utils.timezone import now
from .serializers import ClientOrgSerializer, SalesforceOrgSerializer
from .models import ClientOrg, SalesforceOrg, Token
from redditors.utils import RedditorsUtils
from redditors.serializers import RedditorSerializer
from redditors.models import Redditor


class ClientsUtils(object):
    @staticmethod
    def insert_dummy_client():
        """
        Inserts a dummy client org with related objects and returns token key
        generated.
        """
        salesforce_org_data = {'org_id': '1234567890', 'org_name': 'dummy'}
        serializer = SalesforceOrgSerializer(data=salesforce_org_data)
        serializer.is_valid(raise_exception=True)
        salesforce_org = serializer.save()

        redditor_data = RedditorsUtils.get_dummy_redditor_data()
        serializer = RedditorSerializer(data=redditor_data)
        serializer.is_valid(raise_exception=True)
        redditor = serializer.save()

        serializer = ClientOrgSerializer(
            data={'connected_at': now(), 'reddit_token': None, 'is_active': True}
        )
        serializer.is_valid(raise_exception=True)
        client_org = serializer.save(salesforce_org=salesforce_org, redditor=redditor)
        token = Token.objects.create(client_org=client_org)
        return token.key

    @staticmethod
    def get_redditor_name(client_org=None):
        """
        Receives a ClientOrg instance and return the redditor name linked to this client org.
        """
        if client_org:
            # Looking for the redditor with the id from the client org instance
            redditor = Redditor.objects.get_or_none(id=client_org.redditor_id)
            if redditor:
                return redditor.name
        return None
