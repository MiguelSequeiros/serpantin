from django import newforms as forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.datastructures import MultiValueDict
from util import flatatt, escape_string

class DateTextBox(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name,
            dojoType='dijit.form.DateTextBox', lang='ru-ru', constraints="{datePattern:'dd.MM.yyyy'}", promptMessage="dd.MM.yyyy")
        if value != '': final_attrs['value'] = force_unicode(value) # Only add the 'value' attribute if a value is non-empty.
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

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
        return mark_safe(store + super(FilteringSelectStore, self).render(name, value, attrs))

class FilteringSelect(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super(FilteringSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        attrs.setdefault('dojoType', 'dijit.form.FilteringSelect')
        attrs.setdefault('store', "itemStore")
        attrs.setdefault('searchAttr', "name")
        #attrs.setdefault('query', "{name:'*'}")
        return super(FilteringSelect, self).render(name, value, attrs, choices)

class TagsWidget(forms.Widget):
    def __init__(self, attrs=None, choices=(), tag_widget=forms.TextInput, width=1):
        super(TagsWidget, self).__init__()
        self.choices = choices
        self.tag_widget = isinstance(tag_widget, type) and tag_widget(attrs) or tag_widget
        self.width = width
    
    def render(self, name, value, attrs=None):
        print "TagsWidget.render: ", list(self.choices)
        if value is None: value = []
        id = attrs.pop('id', "tags")
        output = [
            u'<div id="%s">' % id,
            u'</div>',
            u'<script type="text/javascript" src="/site_media/js/tags.js"></script>',
            u'<script type="text/javascript">',
            u'var div = document.createElement("DIV");',
            u"div.innerHTML = '%s'" % self.tag_widget.render(name, None, attrs),
            u'var values = [%s];' % ', '.join(['"' + escape_string(c[1]) + '"' for c in self.choices if c[0] in value]),
            u'addEvent(window, "load",',
            u'\tfunction() {createTagsWidget(document.getElementById("%s"), div.firstChild, values, %s);}' % (id, self.width),
            u');',
            u'</script>'
        ]
        
        return mark_safe(u'\n'.join(output))

    def value_from_datadict(self, data, files, name):
        "This function converts POST data into a widget's value"
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name, None)
