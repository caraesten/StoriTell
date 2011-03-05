from django.core.management.base import BaseCommand, CommandError
from storitell.stories.models import ip_address

# Every 24 hours, this is run to clear IP addresses and maintain
# anonymity. The same script clears the Apache logs too.

class Command(BaseCommand):
	help = 'Clears IP addresses for up/down votes'

	def handle(self, **options):
		addresses = ip_address.objects.all()
		for address in addresses:
			address.delete()
		self.stdout.write("Cleared IPs")
