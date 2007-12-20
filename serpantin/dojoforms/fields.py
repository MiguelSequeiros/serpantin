from django import newforms as forms
from django.db import models
from widgets import DateTextBox, ComboBox, FilteringSelectStore, FilteringSelect, TagsWidget

class DateField(forms.DateField):
    widget = DateTextBox

class ComboField(forms.IntegerField):
    widget = ComboBox
    def __init__(self, **kwargs):
        kwargs.pop('queryset')
        forms.IntegerField.__init__(self, **kwargs)

class FilteringSelectStoreField(forms.Field):
    def __init__(self, queryset, url="", required=True, widget=FilteringSelectStore, label=None, initial=None,
                 help_text=None, error_messages=None):
        #print "initial", initial
        self.queryset = queryset
        super(FilteringSelectStoreField, self).__init__(required, widget, label, initial, help_text, error_messages)
        self.widget.url = url
        
    def clean(self, value):
        forms.Field.clean(self, value)
        if value in ('', None):
            return None
        try:
            value = self.queryset.model._default_manager.get(pk=value)
        except self.queryset.model.DoesNotExist:
            raise ValidationError(ugettext(u'Select a valid choice. That'
                                           u' choice is not one of the'
                                           u' available choices.'))
        return value

class FilteringSelectField(forms.ModelChoiceField):
    def __init__(self, queryset, empty_label=u"---------", cache_choices=False,
                 required=True, widget=FilteringSelect, label=None, initial=None, help_text=None):
        super(FilteringSelectField, self).__init__(queryset, empty_label, cache_choices, required, widget, label, initial, help_text)

class TagsField(forms.ModelMultipleChoiceField):
    def __init__(self, queryset, tag_field=forms.CharField, cache_choices=False, required=True,
                 widget=TagsWidget, label=None, initial=None,
                 help_text=None, *args, **kwargs):
        print "TagsField.__init__: ", initial
        super(TagsField, self).__init__(queryset, cache_choices, required,
              widget, label, initial, help_text, *args, **kwargs)
        self.tag_field = isinstance(tag_field, type) and tag_field() or tag_field
        self.widget.tag_widget = self.tag_field.widget

    def clean(self, value):
        print "TagsField.clean: ", value
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['list'])
        final_values = []
        for val in value:
            val = self.tag_field.clean(val)
            obj, created = self.queryset.get_or_create(name=val)
            final_values.append(obj)
        return final_values

def formfield_callback(field, **kwargs):
    if isinstance(field, models.DateField):
        defaults = {'required': not field.blank}
        defaults.update(kwargs)
        return DateField(**defaults)
    elif isinstance(field, models.ForeignKey):
        meta = field.rel.to._meta
        defaults = {'queryset': field.rel.to._default_manager.all(),
                    'url': '%s/%s/' % (meta.app_label, meta.object_name,),
                    'required': not field.blank}
        #defaults = {'queryset': field.rel.to._default_manager.all()}
        defaults.update(kwargs)
        return FilteringSelectStoreField(**defaults)
        #return FilteringSelectField(**defaults)
    else:
        return field.formfield(**kwargs)
