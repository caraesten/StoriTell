from django.db import models
from django.contrib.comments.models import Comment
from django.core.mail import send_mail
from django.conf import settings
from storitell.stories.models import ip_address

class CommentWithRank(Comment):
    rank = models.IntegerField("Rank", default=0)
    ip_block = models.ManyToManyField(ip_address)
    
    def send_warning_email(self):
        message = 'Comment %s is being heavily downranked. Please moderate!' % (self.id)
        for mod in settings.MODERATORS:
            send_mail('Here be dragons: comment fail!', message, 'admin@storitell.com',[mod[1]], fail_silently=True)
# Create your models here.
