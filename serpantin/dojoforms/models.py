from django import newforms as forms
from django.db import models
import fields

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
        #defaults = {'form_class': forms.ModelMultipleChoiceField}
        defaults.update(kwargs)
        return super(TagsField, self).formfield(**defaults)
