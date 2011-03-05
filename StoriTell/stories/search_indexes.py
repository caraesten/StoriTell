import datetime
from haystack.indexes import *
from haystack import site
from storitell.stories.models import Story

# StoriTell runs with Haystack for search. This is just makes sure there's
# an index of stories.

class StoryIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	pub_date = DateTimeField(model_attr='pub_date')	

	def get_queryset(self):
		return Story.objects.filter(pub_date__lte=datetime.datetime.now())

site.register(Story,StoryIndex)
