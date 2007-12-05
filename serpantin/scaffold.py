#!/usr/bin/env python

from optparse import OptionParser
import sys
import os
import string

__all__ = ('template_for_model', 'list_template_for_model')

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
    
    # FIXME: think of a better construction
    if fields is None:
        try:
            fields = [f for f in meta.admin.fields if f[0] is None][0][1]['fields']
        except (AttributeError, TypeError, LookupError): fields = []
    
    for f in meta.fields + meta.many_to_many:
        if f.editable and (not fields or f.name in fields):
            formfield = formfield_callback(f)
            if formfield: field_list.append(f.name)
    
    model_name = meta.object_name
    form_body = '\n'.join([string.Template(field_template).substitute({'f': f}) for f in field_list])
    
    return string.Template(form_template).substitute(vars())

def list_template_for_model(model, fields=None):
    form_template = \
"""{% load i18n %}
<div class="paneheader">
	<form id="changelist-search">
	<div><!-- DIV needed for valid HTML -->
		<label><img src="/site_media/images/search.gif" alt="Search" /></label>
		<input type="text" size="40" name="q" value="" id="{{ model }}_sbar" />
		<!--input id="{{ model }}_sb" type="submit" value="Go" onClick="javascript:loadListForm('{{ app }}', '{{ model }}');"></input -->
		<input id="{{ model }}_sbut" type="submit" value="Go"></input>
	</div>
	</form>
</div>

<div class="pane2" style="width: 780px; height: 330px;">
	<table id="fplist_{{ win_id }}" class="panelist">
	<thead>
	<tr>
		<th>&nbsp;</th>
		<th>&nbsp;</th>
$table_head
	</tr>
	</thead>
	<tbody>
	{% for obj in obj_list %}
	<tr class="{% cycle row1,row2 %}">
		<td><a href="javascript:loadForm('{{ app }}', '{{ model }}', '{{ obj.id }}', '{{ obj.$title_field }}');">
		<img src="/site_media/images/edit.gif" alt="{% trans 'Edit object' %}"></a></td>
		<td><a href="javascript:confirmDelObj('{{ app }}','{{ model }}','{{ obj.id }}');"><img src="/site_media/images/trash.gif" alt="{% trans 'Delete object' %}"></a></td>
$table_body
	</tr>
	{% endfor %}
	</tbody>
	</table>
</div>

<div id="toolbar" class="footer">
<a href="javascript:loadForm('{{ app }}','{{ model }}');">{% trans 'Add' %}</a>&nbsp;&nbsp;
{% if has_previous %}
	<a href="javascript:loadListForm('{{ app }}','{{ model }}',{{ previous }});"><<<</a>
{% endif %}
	page {{ page }}
{% if has_next %}
	<a href="javascript:loadListForm('{{ app }}','{{ model }}',{{ next }});">>>></a> {% endif %}(total pages: {{ pages }}; records: {{ hits }})
</div>"""
    
    head_field_templates = {
        'ForeignKey': lambda f: "\t\t<th> {%% trans '%s' %%} </th>" % f.rel.to._meta.verbose_name,
        '__default__': lambda f: "\t\t<th> {%% trans '%s' %%} </th>" % f.verbose_name,
        # TODO: try to process non-fields like in django.contrib.admin.templatetags.admin_list
        '__non_field__': lambda field_name: "\t\t<th> {%% trans '%s' %%} </th>" % field_name.replace('_', ' ').capitalize()
    }
    
    head_field_specials = {
        'createuser': lambda f: "\t\t<th> {% trans 'Create' %} </th>",
        'modifyuser': lambda f: "\t\t<th> {% trans 'Mod.' %} </th>"
    }
    
    body_field_templates = {
        'EmailField': lambda f: '\t\t<td><a href="mailto:{{ obj.%(name)s }}">{{ obj.%(name)s }}</a></td>' % {'name': f.name},
        '__default__': lambda f: '\t\t<td>{{ obj.%s }}</td>' % f.name,
        '__non_field__': lambda field_name: '\t\t<td>{{ obj.%s }}</td>' % field_name
    }
    
    body_field_specials = {}
        
    meta = model._meta
    
    from django.db.models import FieldDoesNotExist
    def field_template(field_name, field_templates, field_specials = {}):
        try:
            f = meta.get_field(field_name)
            field_class = f.get_internal_type()
            if field_name in field_specials: return field_specials[field_name](f)
            if not field_class in field_templates: field_class = '__default__'
            return field_templates[field_class](f)
        except FieldDoesNotExist:
            # TODO: probably field existence should be tested here:
            # f = getattr(model, field_name, '')
            return field_templates['__non_field__'](field_name)
    
    # FIXME: think of a better construction
    if fields is None:
        try:
            field_list = meta.admin.list_display
        except (AttributeError, TypeError): field_list = [] # FIXME: maybe should be meta.fields + meta.many_to_many
    else: field_list = fields
    
    # TODO: perhaps should use field_list[0] entirely for displaying titles and field_list[1:] as main columns
    title_field = ''
    if field_list: title_field = field_list[0]
    
    table_head = '\n'.join([field_template(field_name, head_field_templates, head_field_specials) for field_name in field_list])
    table_body = '\n'.join([field_template(field_name, body_field_templates, body_field_specials) for field_name in field_list])
    
    return string.Template(form_template).substitute(vars())

def save_template(template, filename):
    template_file = file(filename, "w")
    template_file.write(template)
    template_file.close()

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
    
    from django.db.models import get_app, get_models, get_model

    parser = OptionParser()
    
    parser.add_option("-a", "--app", dest="app", help="The app which contains the model")
    parser.add_option("-m", "--model", dest="model", help="The model to produce the form for")
    
    options, args = parser.parse_args()
    
    if not options.app:
        parser.print_help()
        sys.exit()

    app = get_app(options.app)
    if options.model: models = [get_model(options.app, options.model)]
    else: models = get_models(app)
    
    #models = getattr(__import__("%s.%s" % (project_name, options.app), {}, {}, ['models']), 'models')
    #model = getattr(models, options.model)
    #base_filename = os.path.join(os.path.dirname(models.__file__), 'templates', options.model)
    
    template_path = os.path.join(os.path.dirname(app.__file__), 'templates')
    for model in models:
        base_filename = os.path.join(template_path, model._meta.object_name)
        
        template = template_for_model(model)
        template_filename = base_filename + '_form.gen.html'
        print "Saving template file:\n", template_filename
        save_template(template, template_filename)
        
        list_template = list_template_for_model(model)
        list_template_filename = base_filename + '_list.gen.html'
        print "Saving list_template file:\n", list_template_filename
        save_template(list_template, list_template_filename)
    
if __name__ == '__main__':
    main()
    