from django.db import models
from django.contrib.contenttypes import generic

import fields
from generic import GenericManyToManyField
from tagging.fields import TagField as _TagField
from tagging.models import Tag

class ComboField(models.ForeignKey):
    def __init__(self, to, to_field=None, **kwargs):
        models.ForeignKey.__init__(self, to, to_field, **kwargs)

    def get_internal_type(self):
        return 'ComboField'

    def value_from_object(self, obj):
        "Returns the value of this field in the given model instance."
        id_value = getattr(obj, self.attname)
        return self.rel.to._default_manager.get(pk=id_value)

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.ComboField}
        defaults.update(kwargs)
        return super(ComboField, self).formfield(**defaults)

class FilteringSelectField(models.ForeignKey):
    def __init__(self, to, to_field=None, **kwargs):
        models.ForeignKey.__init__(self, to, to_field, **kwargs)

    def get_internal_type(self):
        return "FilteringSelectField"

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.FilteringSelectField}
        defaults.update(kwargs)
        return super(FilteringSelectField, self).formfield(**defaults)

class TagsField(models.ManyToManyField):
    def __init__(self, to, **kwargs):
        models.ManyToManyField.__init__(self, to, **kwargs)
    
    def get_internal_type(self):
        return "TagsField"
    
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.TagsField}
        defaults.update(kwargs)
        return super(TagsField, self).formfield(**defaults)

class TagField(_TagField):
    def __init__(self, **kwargs):
        super(TagField, self).__init__(**kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.TagField}
        defaults.update(kwargs)
        return super(TagField, self).formfield(**defaults)
    
    def db_type(self):
        return None

# class TagRel(models.ManyToManyRel):
#     def __init__(self):
#         models.ManyToManyRel.__init__(self, TaggedItem)
    
class TagsRelation(generic.GenericRelation):
    def __init__(self, to, **kwargs):
        generic.GenericRelation.__init__(self, to, **kwargs)
        self.editable = True
    
    def formfield(self, **kwargs):
        #defaults = {'form_class': fields.TagsField, 'queryset': self.rel.to._default_manager.all()}
        defaults = {'form_class': fields.TagsField, 'queryset': Tag._default_manager.all()}
        defaults.update(kwargs)
        # If initial is passed in, it's a list of related objects, but the
        # TagsField takes a list of IDs.
        if defaults.get('initial') is not None:
            defaults['initial'] = [i._get_pk_val() for i in defaults['initial']]
        return super(TagsRelation, self).formfield(**defaults)

    def value_from_object(self, obj):
        "Returns the value of this field in the given model instance."
        #return getattr(obj, self.attname).all()
        return [tagged_item.tag for tagged_item in getattr(obj, self.attname).all()]

# class TagsRelation(models.ManyToManyField):
#     def __init__(self, to, **kwargs):
#         models.ManyToManyField.__init__(self, to, **kwargs)
#     
#     def formfield(self, **kwargs):
#         defaults = {'form_class': fields.TagsField}
#         defaults.update(kwargs)
#         return super(TagsRelation, self).formfield(**defaults)

class GenericTagsField(GenericManyToManyField):
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.TagsField}
        defaults.update(kwargs)
        return super(GenericTagsField, self).formfield(**defaults)
