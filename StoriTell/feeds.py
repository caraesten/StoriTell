from django.contrib.syndication.views import Feed
from storitell.stories.models import Story
from django.template.defaultfilters import truncatewords
from datetime import datetime, timedelta

class LatestEntriesFeed(Feed):
	title = "StoriTell.com recent stories"
	link = "/"
	description = "The latest anonymous stories from StoriTell.com"
	
	def items(self):
		return Story.objects.order_by('-pub_date')[:5]
	def item_title(self, item):
		return truncatewords(item.maintext, 3)
	def item_description(self, item):
		return item.maintext

class TodayPopularFeed(Feed):
	title = "StoriTell.com most popular"
	link = "/popular"
	description = "The most popular anonymous stories from StoriTell.com for the day"
	
	def items(self):
		daydate = datetime.now() - timedelta(days=1)
		return Story.objects.filter(pub_date__range=(daydate, datetime.now())).order_by('-upvotes')[:5]
	def item_title(self, item):
		return truncatewords(item.maintext, 3)
	def item_description(self, item):
		return item.maintext

