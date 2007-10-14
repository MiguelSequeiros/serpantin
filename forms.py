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
    	print "RA3VAT FormLookupField obj type - ", self
        return '<input dojoType="dijit.form.ComboBox" name="%s" value="%s"></input>' % (field_name, data)



class LookupFormField(forms.IntegerField):
    widget = LookupFieldWidget
    def __init__(self, **kwargs):
	#FIXME: temporary commented out
        #if kwargs.has_key('model_class'):
        #    self.model_class = kwargs['model_class']
        #    print "RA3VAT FormLookupField is being initialized...", kwargs
        #    kwargs.pop('model_class')
        print kwargs
        kwargs.pop('queryset')
        forms.IntegerField.__init__(self, **kwargs)




class LookupField(ForeignKey):
    def __init__(self, to, to_field=None, **kwargs):
        ForeignKey.__init__(self, to, to_field, **kwargs)
        print "RA3VAT choices ", self.choices
        self._choices = []
	#if kwargs.has_key('relative_to'):
	#    print "RA3VAT relative_to is set..."
	#    self.relative_to = kwargs['relative_to']

    
    def get_internal_type(self):
        return 'LookupField'


    def formfield(self, **kwargs):
	print "RA3VAT formfield.."
	#FIXME: temporary commented out
        #defaults = {'model_class': self.rel.to}
	defaults = {'form_class': LookupFormField}
	#FIXME:
        #kwargs.pop('queryset')
        defaults.update(kwargs)
        return super(LookupField, self).formfield(**defaults)

