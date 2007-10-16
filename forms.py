from django import newforms as forms
from django.db.models.fields.related import ForeignKey


class DojoDateFieldWidget(forms.TextInput):
    def render(self, field_name, data, attrs=None):
	#FIXME: Converted date does not shown in widget
        try:
            date = "%s/%s/%s" % (data.day,data.month,data.year)
        except:
            date = ''
	    
        return '<input type="text" dojoType="dijit.form.DateTextBox" name="%s" lang="ru" value="%s" promptMessage="dd/mm/yy"></input>' % (field_name, date)



class DojoDateField(forms.DateField):
    widget = DojoDateFieldWidget
    


class LookupFieldWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs',{})
        super(LookupFieldWidget, self).__init__(*args, **kwargs)


    def render(self, field_name, data, attrs=None):
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

