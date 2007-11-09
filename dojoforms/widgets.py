from django import newforms as forms

class DateTextBox(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name,
            dojoType='dijit.form.DateTextBox', lang='ru-ru', constraints="{datePattern:'dd.MM.yyyy'}", promptMessage="dd.MM.yyyy")
        if value != '': final_attrs['value'] = force_unicode(value) # Only add the 'value' attribute if a value is non-empty.
        return u'<input%s />' % flatatt(final_attrs)

class ComboBox(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs',{})
        super(ComboBox, self).__init__(*args, **kwargs)

    def render(self, field_name, data, attrs=None):
        print "Subzero data:", type(data)
        return '<input dojoType="dijit.form.ComboBox" name="%s" value="%s"></input>' % (field_name, data)

class FilteringSelectStore(forms.TextInput):
    def __init__(self, attrs=None, url=""):
        self.url = url
        super(FilteringSelectStore, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        attrs.setdefault('dojoType', 'dijit.form.FilteringSelect')
        attrs.setdefault('store', 'store_%s' % name)
        #store = '<div dojoType="dojo.data.ItemFileReadStore" jsId="store_%s" url="/json/%s" requestMethod="get"></div>\n' % (name, self.url,)
        store = '<div dojoType="CustomQueryReadStore" jsId="store_%s" url="/json/%s" requestMethod="get"></div>\n' % (name, self.url,)
        return store + super(FilteringSelectStore, self).render(name, value, attrs)

class FilteringSelect(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super(FilteringSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        attrs.setdefault('dojoType', 'dijit.form.FilteringSelect')
        attrs.setdefault('store', "itemStore")
        attrs.setdefault('searchAttr', "name")
        #attrs.setdefault('query', "{name:'*'}")
        return super(FilteringSelect, self).render(name, value, attrs, choices)
