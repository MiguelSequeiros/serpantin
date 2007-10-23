from django import newforms as forms
from django.db.models.fields.related import ForeignKey
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy

def escape(html):
    "Return the given HTML with ampersands, double quotes and carets encoded."
    return force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
escape = allow_lazy(escape, unicode)

def flatatt(attrs):
    """
    Convert a dictionary of attributes to a single string.
    The returned string will contain a leading space followed by key="value",
    XML-style pairs.  It is assumed that the keys do not need to be XML-escaped.
    If the passed dictionary is empty, then return an empty string.
    """
    return u''.join([u' %s="%s"' % (k, escape(v)) for k, v in attrs.items()])

#DojoDateField classes
class DojoDateFieldWidget(forms.TextInput):
    def _render(self, field_name, data, attrs=None):
        #FIXME: Converted date does not shown in widget
        try:
            date = "%s/%s/%s" % (data.day,data.month,data.year)
        except:
            date = ''
        
        return '<input type="text" dojoType="dijit.form.DateTextBox" name="%s" lang="ru" value="%s" promptMessage="dd/mm/yy"></input>' % (field_name, date)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name,
            dojoType='dijit.form.DateTextBox', lang='en-gb', constraints="{datePattern:'dd.MM.yyyy'}", promptMessage="dd.MM.yyyy")
        if value != '': final_attrs['value'] = force_unicode(value) # Only add the 'value' attribute if a value is non-empty.
        return u'<input%s />' % flatatt(final_attrs)

class DojoDateField(forms.DateField):
    widget = DojoDateFieldWidget



class LookupFieldWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs',{})
        super(LookupFieldWidget, self).__init__(*args, **kwargs)


    def render(self, field_name, data, attrs=None):
        print "Subzero data:", type(data)
        return '<input dojoType="dijit.form.ComboBox" name="%s" value="%s"></input>' % (field_name, data)



class LookupFormField(forms.IntegerField):
    widget = LookupFieldWidget
    def __init__(self, **kwargs):
        kwargs.pop('queryset')
        forms.IntegerField.__init__(self, **kwargs)



class LookupField(ForeignKey):
    def __init__(self, to, to_field=None, **kwargs):
        ForeignKey.__init__(self, to, to_field, **kwargs)

    def get_internal_type(self):
        return 'LookupField'


    def value_from_object(self, obj):
        "Returns the value of this field in the given model instance."
        id_value = getattr(obj, self.attname)
        return self.rel.to._default_manager.get(pk=id_value)


    def formfield(self, **kwargs):
        defaults = {'form_class': LookupFormField }
        defaults.update(kwargs)
        return super(LookupField, self).formfield(**defaults)

# FilteringSelect classes
class FilteringSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super(FilteringSelectWidget, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        attrs.setdefault('dojoType', 'dijit.form.FilteringSelect')
        return super(FilteringSelectWidget, self).render(name, value, attrs, choices)

class FilteringSelectFormField(forms.ModelChoiceField):
    def __init__(self, queryset, empty_label=u"---------", cache_choices=False,
            required=True, widget=FilteringSelectWidget, label=None, initial=None, help_text=None):
        super(FilteringSelectFormField, self).__init__(queryset, empty_label, cache_choices, required, widget, label, initial, help_text)

class FilteringSelectField(ForeignKey):
    def __init__(self, to, to_field=None, **kwargs):
        ForeignKey.__init__(self, to, to_field, **kwargs)

    def get_internal_type(self):
        return "FilteringSelectField"

    def formfield(self, **kwargs):
        defaults = {'form_class': FilteringSelectFormField}
        defaults.update(kwargs)
        return super(FilteringSelectField, self).formfield(**defaults)
