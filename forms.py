from django import newforms as forms



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
    


