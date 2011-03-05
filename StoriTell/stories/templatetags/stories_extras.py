from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from storitell.cust_comments.models import CommentWithRank
from storitell.quotes.models import Quote
import re

register = Library()

# Code via Paolo Bergantino on StackOverflow
# http://stackoverflow.com/questions/721035/django-templates-stripping-spaces
# Used under CC-By-Sa 2.5.
@stringfilter
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))
spacify.needs_autoescape = True
register.filter(spacify)

@register.inclusion_tag('templatetags/chatter.html')
def show_chatter():
    try:
        comments = CommentWithRank.objects.filter(is_public=True).filter(rank__gte=-4).order_by('-submit_date')[:3]
    except:
        comments = ""
    return {'comments': comments}

@register.inclusion_tag('templatetags/quote.html')
def show_quote():
    try:
        quote = Quote.objects.all().order_by('?')[:1]
    except:
        quote = ""
    return {'quote': quote}
    
@register.inclusion_tag('templatetags/analytics.html')
def show_analytics():
    data = " "
    return {'data': data}