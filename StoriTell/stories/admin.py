from storitell.stories.models import *
from django.contrib import admin

# Honestly, the only thing the Django admin is really used
# for is moderation. So, kinda want to keep this as simple
# as possible.

admin.site.register(Story)
admin.site.register(ip_address)