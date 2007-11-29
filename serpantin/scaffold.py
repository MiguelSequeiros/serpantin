#!/usr/bin/env python

from optparse import OptionParser
import sys
import os
import string

__all__ = ('template_for_model',)

def template_for_model(model, fields=None, formfield_callback=lambda f: f.formfield()):
    # TODO: try to generate a template from a form class, using form.base_fields
    form_template = \
"""{% load i18n %}
<div class="$model_name">
<form id="fpform_{{ win_id }}" app="common" model="$model_name" oid="{{obj.id}}" class="fpform" method="POST">
<table>
$form_body
<tr><td colspan="2">
<div class="box">
<button dojoType="dijit.form.Button"
	onclick="submitForm('common', '$model_name', '{{ object_id }}', '{{ win_id }}', 'save');">
	<span>Save and continue</span></button>
<button dojoType="dijit.form.Button"
	onclick="this.setDisabled(true); submitForm('common', '$model_name', '{{ object_id }}', '{{ win_id }}', 'save_and_close');">
	<span>Save</span>
</button>
</div>
</td></tr>

<!-- FIXME: get rid of those -->
<tr><td colspan="2">
<input type="hidden" name="createuser" value="1">
<input type="hidden" name="modifyuser" value="1">
{% if debug %}
<input type="submit">
{% endif %}
</td></tr>

</table> 
</form>

<p>{% if obj.createdate %}
		{% trans 'Createdata:' %} {{obj.createdate|date:"F j, Y"}}
		{{obj.createuser.username}}<br/>
    {% endif %}
    {% if obj.modifydate %}
		{% trans 'Modifydata:' %} {{obj.modifydate|date:"F j, Y"}}
		{{obj.modifyuser.username}}<br/>
    {% endif %}

</p><p>&nbsp;</p>
</div>"""
    
    field_template = \
"""<tr>
    <td>{{ form.$f.label_tag }}</td>
    <td>
        {{ form.$f }}
        {% if field.help_text %}{{ field.help_text }}{% endif %}
        {% if field.errors %}{{ field.errors }}{% endif %}
    </td>
</tr>"""
    
    meta = model._meta
    field_list = []
    for f in meta.fields + meta.many_to_many:
        if not f.editable: continue
        if fields and not f.name in fields: continue
        formfield = formfield_callback(f)
        if formfield: field_list.append(f.name)
    
    model_name = meta.object_name
    form_body = ''.join([string.Template(field_template).substitute({'f': f}) for f in field_list])
    
    return string.Template(form_template).substitute(vars())

def main():
    try:
        import settings
    except ImportError:
        print "Settings file not found.  Place this file in the same place as manage.py"
        sys.exit()
    
    project_directory = os.path.dirname(settings.__file__)
    project_name = os.path.basename(project_directory)
    sys.path.append(os.path.join(project_directory, '..'))
    project_module = __import__(project_name, '', '', [''])
    sys.path.pop()
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % project_name
    
    parser = OptionParser()
    
    parser.add_option("-a", "--app", dest="app", help="The app which contains the model")
    parser.add_option("-m", "--model", dest="model", help="The model to produce the form for")
    
    options, args = parser.parse_args()
    
    if not (options.model and options.app):
        parser.print_help()
        sys.exit()
    
    model = getattr(__import__("%s.%s.models" % (project_name, options.app), '', '', [options.model]), options.model)
    print template_for_model(model)

if __name__ == '__main__':
    main()
    