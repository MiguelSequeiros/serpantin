from django.db import models

from serpantin.dojoforms.models import TagsField #, TagField
from tagging.fields import TagField

class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
        
class Article(models.Model):
    name = models.CharField(max_length=100)
    #tags = TagsField(Tag)
    tags = TagField()
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
