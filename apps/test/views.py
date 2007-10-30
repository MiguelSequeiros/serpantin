from django.http import HttpResponse
from django.shortcuts import render_to_response
from serpantin.apps.common.models import Town

import simplejson

class JsonResponse(HttpResponse):
    def __init__(self, obj):
        self.original_obj = obj
        HttpResponse.__init__(self, self.serialize())
        self["Content-Type"] = "text/javascript"

    def serialize(self):
        return("/*" + simplejson.dumps(self.original_obj) + "*/")

def test(request):
    print "Subzero POST data:", request.POST
    return render_to_response('query.html', {})

def model_store(app_name, model_name, query = ""):
    #FIXME: get rid of serpantin.apps in getattr
    model = getattr(__import__('serpantin.apps.%s.models' % app_name, '', '', [model_name]), model_name)
    if len(query) and query[-1] == '*': query = query[:-1]
    objects_filtered = model.objects.filter(name__istartswith=query)
    return [{'name':i.name, 'id':i.id} for i in objects_filtered]
    
def json(request):
    content = [
        {
            'name':'Alabama',
            'label':'Alabama',
            'abbreviation':'AL',
        },
        {
            'name':'Alaska',
            'label':'Alaska',
            'abbreviation':'AK',
        },
        {
            'name':'American Samoa',
            'label':'American Samoa',
            'abbreviation':'AS',
        },
    ]
    print "Subzero GET data:", request.GET
    query = ""
    if 'q' in request.GET: query = request.GET['q']
    #if len(query) and query[-1] == '*': query = query[:-1]
    #result = [i for i in content if not (query and i['name'].lower().find(query.lower()))]
    result = model_store('common', 'Town', query)
    
    return JsonResponse({'identifier':'id', 'label':'name', 'items':result})

def _json(request):
    return render_to_response('test.json', {})
