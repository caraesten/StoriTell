from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator
from storitell.stories.models import Story
from django.template import RequestContext
from django.template.defaultfilters import *
from django.contrib.comments.models import Comment
from storitell.beta_codes.models import code
from datetime import datetime, timedelta
from itertools import chain

def first_auth(request):
        return redirect("main-page")

# Stories are displayed by default with the most popular stories over the
# last three days making up the first three, and then the most recent excluding
# those under it.
def main(request, page_num=1, order='home'):
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1
    if order == 'home':
        todayDate = datetime.now().date() - timedelta(days = 3)
        storiesPopA = Story.objects.filter(pub_date__gte=todayDate).order_by('-upvotes').values_list('id', flat=True)[:3]
        storiesPopB = Story.objects.filter(id__in=storiesPopA).order_by('-upvotes')
        storiesRest = Story.objects.all().exclude(id__in=storiesPopA).order_by('-pub_date')
        stories = list(chain(storiesPopB, storiesRest))
    elif order == 'recent':
        stories = Story.objects.all().order_by('-pub_date')
    elif order == 'popular':
        stories = Story.objects.all().order_by('-upvotes')
    elif order == 'popular-week':
        weekdate = datetime.now() - timedelta(days=7)
        stories = Story.objects.filter(pub_date__range=(weekdate, datetime.now())).order_by('-upvotes')
    for story in stories:
        story.title = truncatewords_html(story.maintext, 3)
    p = Paginator(stories, 5)
    page = p.page(page_num)
    comments = Comment.objects.filter(is_public=True).order_by('-submit_date')[:3]
    return render_to_response('index.html',{'stories':page, 'comments':comments}, context_instance=RequestContext(request))

def single(request, post_id, story_slug):
    try:
        story = Story.objects.get(id=post_id)
    except:
        raise Http404
    comments = Comment.objects.filter(is_public=True).order_by('-submit_date')[:3]
    return render_to_response('single.html',{'Story':story, 'comments': comments},context_instance=RequestContext(request))

def clear_user(request):
    try:
        request.session.clear()
        return HttpResponseRedirect("/")
    except:
        return HttpResponseRedirect("/")
    
