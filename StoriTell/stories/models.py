from django.db import models
from django.template.defaultfilters import slugify
from storitell.extra import unique_slugify
from datetime import datetime
from django.contrib.comments.signals import comment_was_posted
from django.utils.encoding import smart_str
from django.core.mail import mail_managers
import akismet
from django.conf import settings
from django.contrib.sites.models import Site


class ip_address(models.Model):
    address = models.CharField(max_length=25)
    def __unicode__(self):
        return '%s' % (self.address)
#   Store IPs as objects to use Django queries to check for repeats.

class Story(models.Model):
    maintext = models.TextField("Story")
    upvotes = models.PositiveIntegerField("Upvotes", default=0, help_text="The rating of the story, as determined by visitors.")
    pub_date = models.DateTimeField(editable=False, auto_now_add=True)
    slug = models.SlugField(editable=False)
    ip_block = models.ManyToManyField(ip_address, blank=True) # Blocked IPs can't upvote a story. Cleared every 24 hrs
    def save(self):
        if not self.id:
            self.pub_date = datetime.now()
        unique_slugify(self, self.maintext) # make sure slug is unique
        super(Story, self).save()
        return True
    def get_absolute_url(self):
        return "/stories/%s/%s" % (self.id, self.slug)
    def __unicode__(self):
        return '%s' % (self.slug)
    def moderate_comment(sender, comment, request, **kwargs):
        ak = akismet.Akismet(
            key = settings.AKISMET_API_KEY,
                blog_url = 'http://%s/' % Site.objects.get_current().domain
        )
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', ''),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERRER', ''),
            'comment_type': 'comment',
        }
        if ak.comment_check(smart_str(comment.comment), data=data, build_data=True):
            comment.is_public = False
            comment.save()
    
        if comment.is_public:   
            email_body = "%s"
            mail_managers ("New comment posted", email_body % (comment.get_as_text()))
	comment_was_posted.connect(moderate_comment)
    class Meta:
        verbose_name_plural = "Stories"
        verbose_name = "Story"
    
