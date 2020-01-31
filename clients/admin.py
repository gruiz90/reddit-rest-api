from django.contrib import admin
from .models import ClientOrg, SalesforceOrg, Token

admin.site.register(ClientOrg)
admin.site.register(SalesforceOrg)
admin.site.register(Token)
