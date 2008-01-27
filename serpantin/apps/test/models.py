from django.db import models
from django.contrib.contenttypes import generic

from serpantin.dojoforms.models import TagsField, TagField, TagsRelation
#from tagging.fields import TagField
from tagging.models import TaggedItem

class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
        
class Article(models.Model):
    name = models.CharField(max_length=100)
    tags = TagsField(Tag)
    #tags = TagField()
    #tags = TagsRelation(TaggedItem)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
