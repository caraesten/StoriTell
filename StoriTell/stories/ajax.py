from django.template import Context, loader
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.core.mail import send_mail
from storitell.stories.models import Story
from django.template import RequestContext
from storitell.cust_comments.models import CommentWithRank
from storitell.stories.models import ip_address
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str
from django.db.models import Q
from time import strftime
from storitell.stories.extra_methods import moderate_comment
import datetime
import hashlib
import akismet
import re

def addStory(request):
		text = smart_str(request.POST.get('storytext', False))
		
#       Not a fan of people posting images to StoriTell, especially
#       when Markdown formatting is enabled. Search for images,
#       and remove them.
		
		regex1 = r'\!\[.*\)'
		text = re.sub(regex1,' ',text)
		text = re.sub(r'\[id\].*jpg|png|gif|tif|jpeg|tiff',' ',text)
		if text:
				try:
					Story.objects.get(maintext=text)
					response = "repeat"

#                   Don't allow repeat stories.

				except:
					entry = Story(maintext=text, pass1='', pass2='')
					responseSpam = moderate_comment(text, request)
					if responseSpam == False:
							if entry.save():
								   response = "success"
							else:
								   response = "fail"
					else:
					   response = "spam"
		else:
				response = "fail"
		return HttpResponse(response, mimetype='application/JavaScript')

def commentVote(request):
	commentID = request.POST.get('commentID', False)
	commentAction = request.POST.get('commentAct',False)
	try:
		comment = CommentWithRank.objects.get(id=commentID)
	except:
		raise Http404
	thisip = request.META['HTTP_X_FORWARDED_FOR']
	ip_addr = ip_address.objects.get_or_create(address=thisip)

#   Temporarily store IP so people can't repeatedly like a comment,
#   artificially upvoting it.

	if commentAction == "Up":
		if comment.ip_block.filter(address=thisip).count() == 0:
			comment.rank += 1
			comment.ip_block.add(ip_addr[0])
			comment.save()
			response = "success"
		else:
			response = "ip_blocked"
	elif commentAction == "Down":
		if comment.ip_block.filter(address=thisip).count() == 0:
			comment.rank -= 1
			comment.ip_block.add(ip_addr[0])
			if comment.rank < -3:
				comment.send_warning_email()
			comment.save()
			response = "success"
		else:
			response = "ip_blocked"
	else:
		response = "failure. No action."
	return HttpResponse(response, mimetype='application/JavaScript')

def storyVote(request):
	storyID = request.POST.get('storyID',False)
	try:
		story = Story.objects.get(id=storyID)
	except:
		raise Http404
	thisip = request.META['HTTP_X_FORWARDED_FOR']
	ip_addr = ip_address.objects.get_or_create(address=thisip)

#   Same as for comments, store IP to prevent repeated upvotes

	if story.ip_block.filter(address=thisip).count() == 0:
		story.upvotes += 1
		story.ip_block.add(ip_addr[0])
		story.save()
		response = "success"
	else:
		response = "ip_blocked"
	return HttpResponse(response, mimetype='application/JavaScript')

def reportStory(request):
	storyID = request.POST.get('storyID',False)
	try:
		story = Story.objects.get(id=storyID)
	except:
		raise Http404
	submitted = datetime.datetime.today().strftime("%m/%d/%Y %H:%M")
	subject = "Story reported at: %s" % (submitted)
	message = "Story text:\n %s" % (story.maintext)
	to = []
	for person in settings.MANAGERS:
		to.append(person[1])
	send_mail(subject, message, 'admin@storitell.com',to,fail_silently=True)
	return HttpResponse('success', mimetype='application/JavaScript')
	
