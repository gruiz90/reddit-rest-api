from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions
from django.core.cache import cache

from herokuredditapi.utils import Utils
logger = Utils.init_logger(__name__)


class MyOauthConfirmPermission(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in SAFE_METHODS:
        #     return True

        logger.info(request.user)
        state = request.query_params.get('state')
        if not state:
            raise exceptions.ParseError(
                detail={'detail': 'state param not found'})
        oauth_data = cache.get(f'oauth_{state}')
        if not oauth_data:
            raise exceptions.PermissionDenied(
                detail={'detail': 'Invalid or expired state'})
        else:
            if request.method == 'POST' and oauth_data['status'] != 'accepted':
                raise exceptions.PermissionDenied(
                    detail={'detail': 'Authorization still pending.'})

        # Write permissions are only allowed to the owner of the snippet.
        # return obj.owner == request.user
        return True
