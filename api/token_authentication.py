from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from clients.models import Token
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class MyTokenAuthentication(TokenAuthentication):
    """
	A simple token based authentication. Adapted to used my Token model implementation.

	Clients should authenticate by passing the token key in the "Authorization"
	HTTP header, prepended with the string "Bearer ".  For example:

		Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
	"""

    keyword = 'Bearer'
    model = Token

    def authenticate_credentials(self, key):
        """
		Almost the same method as upper TokenAuthentication class, but using Client Org.
		"""
        model = self.get_model()
        try:
            token = model.objects.select_related('client_org').get(key=key)
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.client_org.is_active:
            raise exceptions.AuthenticationFailed(_('Client org inactive or deleted.'))

        token.client_org.is_authenticated = True
        return (token.client_org, token)
