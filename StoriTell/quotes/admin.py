from storitell.quotes.models import *
from django.contrib import admin

class QuoteAdmin(admin.ModelAdmin):
	raw_id_fields = ('sFrom',)
admin.site.register(Quote, QuoteAdmin)
