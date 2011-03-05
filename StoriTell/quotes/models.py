from django.db import models
from django.template.defaultfilters import slugify
from storitell.extra import unique_slugify
from storitell.stories.models import Story


# Create your models here.
class Quote(models.Model):
    text = models.TextField("Quote")
    slug = models.SlugField(editable=False)
    sFrom = models.ForeignKey('stories.Story')
    def save(self):
        unique_slugify(self, self.text)
        super(Quote, self).save()
        return True
    def get_absolute_url(self):
        return "/stories/%s/%s" % (self.id, self.slug)
    def __unicode__(self):
        return '%s' % (self.slug)


