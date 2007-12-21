from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.utils.safestring import mark_safe

# JSON srore classes
def model_query(model, query = ""):
    if len(query) and query[-1] == '*': query = query[:-1]
    objects_filtered = model.objects.filter(name__istartswith=query)
    items = [{'name':i.name, 'id':i.id} for i in objects_filtered]
    return {'identifier':'id', 'items':items}

def model_id(model, id):
    object = model.objects.get(pk=id)
    return {'identifier':'id', 'items':[{'name':object.name, 'id':object.id}]}

# Misc functions
def escape(html):
    "Return the given HTML with ampersands, double quotes and carets encoded."
    return mark_safe(force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))
escape = allow_lazy(escape, unicode)

def escape_string(string):
    "Return the given string with backslashes and double quotes escaped"
    return mark_safe(force_unicode(string).replace('\\', '\\\\').replace('"', '\\"'))
    
def flatatt(attrs):
    """
    Convert a dictionary of attributes to a single string.
    The returned string will contain a leading space followed by key="value",
    XML-style pairs.  It is assumed that the keys do not need to be XML-escaped.
    If the passed dictionary is empty, then return an empty string.
    """
    return u''.join([u' %s="%s"' % (k, escape(v)) for k, v in attrs.items()])
