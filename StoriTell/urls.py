from django.conf.urls.defaults import *
from storitell.feeds import LatestEntriesFeed, TodayPopularFeed
from django.contrib.comments.feeds import LatestCommentFeed
from storitell.stories.api import StoryResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

story_resource = StoryResource()

urlpatterns = patterns('',
	# Example:
	# (r'^storitell/', include('storitell.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^$','storitell.stories.views.first_auth', name="bauth-page"),
	url(r'^clearsession/$','storitell.stories.views.clear_user', name="clear-user"),
	url(r'^home/$','storitell.stories.views.main', name="main-page"), 
	url(r'^home/recent/$','storitell.stories.views.main',{'order':'recent'}, name="recent-stories"),
	url(r'^popular/$','storitell.stories.views.main',{'order':'popular'}, name="popular_stories"),
	url(r'^popular/thisweek/$','storitell.stories.views.main',{'order':'popular-week'}, name="popular_stories_week"),
	url(r'^stories/(?P<post_id>\d+)/(?P<story_slug>[-\w]+)/$', 'storitell.stories.views.single'),
	(r'^comments/', include('django.contrib.comments.urls')),
	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	
	#ajax URLs
	url(r'^addStory/', 'storitell.stories.ajax.addStory', name="submit_story"),
	url(r'^ajax/commentVote/', 'storitell.stories.ajax.commentVote', name="comment_vote"),
	url(r'^ajax/storyVote/','storitell.stories.ajax.storyVote', name="story_vote"),
	url(r'^deleteStory/', 'storitell.stories.ajax.deleteStory', name="delete_story"),
	url(r'^reportStory/', 'storitell.stories.ajax.reportStory', name="report_story"),

	#feeds
	(r'^latest/feed/$', LatestEntriesFeed()),
	(r'^popular/feed/$', TodayPopularFeed()),

	#static content
	url(r'^about/$','django.views.generic.simple.direct_to_template',{'template':'static/about.html'}),
	url(r'^legal/$','django.views.generic.simple.direct_to_template',{'template':'static/legal.html'}),
	url(r'^help/$','django.views.generic.simple.direct_to_template',{'template':'static/help.html'}),


	#api
	(r'api/', include(story_resource.urls)),
	
	#other
	(r'^search/', include('haystack.urls')),
)
