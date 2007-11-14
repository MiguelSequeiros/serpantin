from django import newforms as forms
from django.db import models
from widgets import DateTextBox, ComboBox, FilteringSelectStore, FilteringSelect

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

def formfield_callback(field, **kwargs):
    if isinstance(field, models.DateField):
        return DateField(**kwargs)
    elif isinstance(field, models.ForeignKey):
        print "form_callback", kwargs
        meta = field.rel.to._meta
        defaults = {'queryset': field.rel.to._default_manager.all(), 'url': '%s/%s/' % (meta.app_label, meta.object_name,)}
        defaults.update(kwargs)
        return FilteringSelectStoreField(**defaults)
    else:
        return field.formfield(**kwargs)
