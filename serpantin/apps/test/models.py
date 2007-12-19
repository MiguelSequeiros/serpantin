from django.db import models

from serpantin.dojoforms.models import TagsField

class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
        
class Article(models.Model):
    name = models.CharField(max_length=100)
    tags = TagsField(Tag)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
