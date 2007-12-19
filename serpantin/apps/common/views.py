from django.db.models.query import Q, QOr

from django.core.paginator import ObjectPaginator
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context, Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.forms import FormWrapper
from django.http import HttpResponse, HttpResponseRedirect

from django.db import models
from django.newforms import form_for_model, form_for_instance

from serpantin.dojoforms import *
from serpantin.scaffold import template_for_model, list_template_for_model

import simplejson
import os

# Helpers
def get_model(app_name, model_name):
    # FIXME make use of django.db.models.loading.get_model, like in the admin interface
    return getattr(__import__('serpantin.apps.%s.models' % app_name, {}, {}, [model_name]), model_name)

def get_template_dir(app_name):
    # FIXME do it like in django.db.models.loading.get_app
    app = 'serpantin.apps.' + str(app_name)
    i = app.rfind('.')
    if i == -1:
        m, a = app, None
    else:
        m, a = app[:i], app[i+1:]
    if a is None:
        mod = __import__(m, {}, {}, [])
    else:
        mod = getattr(__import__(m, {}, {}, [a]), a)
    return os.path.join(os.path.dirname(mod.__file__), 'templates')

class JsonResponse(HttpResponse):
    def __init__(self, obj):
        self.original_obj = obj
        HttpResponse.__init__(self, self.serialize())
        self["Content-Type"] = "text/javascript"

    def serialize(self):
        return("/*" + simplejson.dumps(self.original_obj) + "*/")

def json(request, app_name, model_name):
    print "json GET data:", request.GET
    query = ""
    if 'q' in request.GET: query = request.GET['q']
    id = ""
    if 'id' in request.GET: 
        try: id = int(request.GET['id'])
        except ValueError: id = ""

    model = getattr(__import__('serpantin.apps.%s.models' % app_name, '', '', [model_name]), model_name)
    result = id != "" and model_id(model, id) or model_query(model, query)
    
    return JsonResponse(result)

def async_list(request, app_name, model_name):
    # FIXME: commented checking on anonymous
    # if not request.user.is_anonymous():
    print "async_list"
    model = get_model(app_name, model_name)
    meta = model._meta
    query = request.GET.get('q', '')
    q_list = []
    if query:
        search_fields = meta.admin.search_fields
        for field_name in search_fields:
            field = meta.get_field(field_name)
            # TODO: add here model fields list exported from dojoforms.models
            if field.get_internal_type() not in ['ForeignKey']:
                q_list.append(Q(**{'%s__icontains' % field_name: query}))
            else:
                for rel_field_name in field.rel.to._meta.admin.search_fields:
                    q_list.append(Q(**{'%s__%s__icontains' % (field_name, rel_field_name): query}))
    q = QOr(*q_list)
    try:
        order_field = model._meta.ordering[0]
    except IndexError:
        order_field = '-modifydate'
    queryset = model.objects.filter(q).order_by(order_field)
    paginate_by = int(request.GET.get('count', 10))
    paginator = ObjectPaginator(queryset, paginate_by)
    page = int(request.GET.get('page', 0))
    obj_list = paginator.get_page(page)
    
    params = {
        'is_paginated': paginator.pages > 1,
        'results_per_page': paginate_by,
        'has_next': paginator.has_next_page(page),
        'has_previous': paginator.has_previous_page(page),
        'page': page + 1,
        'next': page + 1,
        'previous': page - 1,
        'pages': paginator.pages,
        'hits' : paginator.hits,
        'is_owner': True,
        'obj_list': obj_list,
        'app': app_name,
        'model': model_name,
    }
    template_name = '%s/%s_list.html' % (get_template_dir(app_name), model_name)
    try:
        template = get_template(template_name)
    except TemplateDoesNotExist:
        template = Template(list_template_for_model(model))
    context = RequestContext(request, params)
    return HttpResponse(template.render(context))
    #return render_to_response(template_name, params, context_instance=RequestContext(request))

def async_delete(request, app_name, model_name, object_id):
    model = get_model(app_name, model_name)
    object = get_object_or_404(model, pk=object_id)
    object.delete()
    return HttpResponseRedirect('/async/%(app_name)s/%(model_name)s/new/' % vars())

def async_form(request, app_name, model_name, object_id='', win_id=''):
    print "async_form POST data:\n", request.POST
    model = get_model(app_name, model_name)
    if object_id:
        object = get_object_or_404(model, pk=object_id)
        Form = form_for_instance(object, formfield_callback=formfield_callback)
    else: Form = form_for_model(model, formfield_callback=formfield_callback)
    auto_id = "id_%s"
    if win_id: auto_id += "_" + win_id
    if request.method == 'POST':
        form = Form(request.POST, auto_id=auto_id)
        if form.is_valid(): form.save()
        else:
            errors = form.errors
            return render_to_response('%s/errors.html' % get_template_dir(app_name), {'errors': errors})
        #return HttpResponseRedirect('/async/%(app_name)s/%(model_name)s/%(object_id)s/%(win_id)s/' % vars())
        return JsonResponse({'result': 'OK'})
    else:
        form = Form(auto_id=auto_id)
        #print form['town']
        params = {
            'debug': False,
            'form': form,
            'edit_object': False,
            'is_owner': True,
            'app': app_name,
            'model': model_name,
            'win_id': win_id,
            'object_id': object_id,
        }
        template_name = '%s/%s_form.html' % (get_template_dir(app_name), model_name)
        try:
            template = get_template(template_name)
        except TemplateDoesNotExist:
            template = Template(template_for_model(model))
        context = RequestContext(request, params)
        return HttpResponse(template.render(context))
        #return render_to_response(template_name, params, context_instance=RequestContext(request))
        
