from django.db.models.query import QOr

from django.core.paginator import ObjectPaginator
from django.shortcuts import render_to_response
from django.template import RequestContext

from serpantin.settings import user

def async_listform(request, app_name, model_name, node):
#FIXME: commented checking on anonymous
#  if not request.user.is_anonymous():
    #model = meta.get_module(app_name, model_name)
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
        'node': node,
    }
   
    print "before render_to_response"
   
    #if 1:
    try:
        tmpl = '%s/apps/%s/templates/%s_list.html' % (user['projectdir'], app_name, model_name) 
        return render_to_response(tmpl, params, context_instance=RequestContext(request))
    except:
        tmpl = '%s/apps/%s/templates/%s_list.gen.html' % (user['projectdir'], app_name, model_name) 
        print "before render_to_response final"
	
        return render_to_response(tmpl, params, context_instance=RequestContext(request))

