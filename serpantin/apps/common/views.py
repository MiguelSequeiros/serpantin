from django.db.models.query import Q,QOr

from django.core.paginator import ObjectPaginator
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms import FormWrapper
from django.http import HttpResponse, HttpResponseRedirect

from django.db import models
from django.newforms import form_for_model
from django.newforms import form_for_instance

from serpantin.settings import PROJECT_DIR
from serpantin.dojoforms import *

import simplejson
import os

# Helpers
def get_model(app_name, model_name):
    # FIXME make use of django.db.models.loading.get_model, like in the admin interface
    return getattr(__import__('serpantin.apps.%s.models' % app_name, '', '', [model_name]), model_name)

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
    # model = meta.get_module(app_name, model_name)
    print "RA3VAT app_name ", app_name
    print "RA3VAT model_name ", model_name
    model = getattr(__import__('serpantin.apps.%s.models' % (app_name), '', '', [model_name]), model_name)
    print "RA3VAT model ", model
    #obj_list = model.get_list(order_by=(['-createdate']))
    obj_list = []
    paginator = None
    if 1:
#    try:
        paginate_by = 10
        q = request.GET.get('q','')
        #FIXME: order_by does not work
        #prop ={'order_by': ['-createdate']}
        prop = {}
        ql = []
        
        if q:
            try:
                #flds = model._meta.admin.list_display
                flds = tuple(model._meta.admin.search_fields)
            except:
                flds = tuple()
            #	print "Fields ", flds[1:]	  
            #	key = '%s__icontains' % flds[0]
            #	kwargs = {key:q} 
            print "RA3VAT flds ", flds
            for f in flds:
                if not  model._meta.get_field(f).get_internal_type() in ['ForeignKey','LookupField']:
                    ql.append(Q(**{'%s__icontains' % f:q}))
                else:
                    for fkf in tuple(model._meta.get_field(f).rel.to._meta.admin.search_fields):
                        kw = {'%s__%s__icontains' % (f, fkf):q}
                        ql.append(Q(**kw))
        print "RA3VAT ql ", ql
        ResQ = QOr(*ql)
        print "RA3VAT ResQ ", ResQ
        #if model._meta.__dict__.has_key('ordering'):
        try:
            order_field = model._meta.ordering[0]
        except:
            order_field = '-modifydate'
	print "RA3VAT before queryset"
        queryset = model.objects.filter(ResQ).order_by(order_field)
        paginator = ObjectPaginator(queryset, 10)
        page = int(request.GET.get('page',0))
	#page = 0
	print "before obj_list"
        try:
            obj_list = paginator.get_page(page)
        except:		
            print "obj_list ", obj_list
#    except:
#        raise Http404
    
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
   
    print "before render_to_response"
   
    #if 1:
    try:
        tmpl = '%s/apps/%s/templates/%s_list.html' % (PROJECT_DIR, app_name, model_name) 
        return render_to_response(tmpl, params, context_instance=RequestContext(request))
    except:
        tmpl = '%s/apps/%s/templates/%s_list.gen.html' % (PROJECT_DIR, app_name, model_name) 
        print "before render_to_response final"

        return render_to_response(tmpl, params, context_instance=RequestContext(request))

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
        print form['town']
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
        template = '%s/%s_form.html' % (get_template_dir(app_name), model_name)
        return render_to_response(template, params, context_instance=RequestContext(request))
