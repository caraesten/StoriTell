from storitell.tastypie.resources import ModelResource
from storitell.stories.models import Story
from storitell.stories.extra_methods import moderate_comment
from storitell.tastypie.validation import Validation

# Stories can be read through a REST-ful interface. It'd be nice
# to be able to POST as well, but that requires validation I haven't
# had time to code yet. Want to add it? Be my guest.

class StoryResource(ModelResource):
	class Meta:
		queryset = Story.objects.all()
		resource_name = 'story'
		fields = ['maintext','pub_date','upvotes']
		allowed_methods = ['get']

