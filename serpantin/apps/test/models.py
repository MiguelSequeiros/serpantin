from django.db import models
from django.contrib.contenttypes import generic

from serpantin.dojoforms.models import TagsField, TagField, TagsRelation, GenericTagsField
from serpantin.dojoforms.generic import GenericManyToManyField
#from tagging.fields import TagField
from tagging.models import TaggedItem, Tag

# class Tag(models.Model):
#     name = models.CharField(max_length=30)
#     
#     def __unicode__(self):
#         return self.name
#     
#     class Admin:
#         pass

class Article(models.Model):
    name = models.CharField(max_length=100)
    #tags = GenericTagsField(Tag, db_table="tagging_taggeditem")
    tags = GenericManyToManyField(Tag, db_table="tagging_taggeditem")
    #tags = TagField()
    #tags = TagsRelation(TaggedItem)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
