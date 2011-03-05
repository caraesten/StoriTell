from django.conf import settings
from django.utils.encoding import smart_str
from time import strftime
from django.contrib.sites.models import Site
import datetime
import akismet

# Storing this in another file because it's useful for API validation

def moderate_comment(comment, request):
	ak = akismet.Akismet(
		key = settings.AKISMET_API_KEY,
			blog_url = 'http://%s/' % Site.objects.get_current().domain
)
	data = {
		'user_ip': request.META.get('REMOTE_ADDR', ''),
		'user_agent': request.META.get('HTTP_USER_AGENT', ''),
		#'referrer': request.META.get('HTTP_REFERRER', ''), ADD THIS AT LAUNCH
		'comment_type': 'comment',
	}
	spamtest = ak.comment_check(comment, data=data, build_data=True)
	return spamtest
