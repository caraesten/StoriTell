import sys
import os
from django.core.management import setup_environ
import settings
setup_environ(settings)
from stories.models import ip_address

addresses = ip_address.objects.all()
for address in addresses:
	address.delete()
