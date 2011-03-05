from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.forms import CommentForm
from storitell.cust_comments.models import CommentWithRank

class CommentFormNew(CommentForm):
    email = forms.EmailField(label=_("Email address"), required=False)
    name = forms.CharField(label=_("Name"), max_length=50, required=False)
    
    def get_comment_model(self):
        return CommentWithRank