from django.http import HttpResponse
from django.shortcuts import render_to_response

import simplejson

class JsonResponse(HttpResponse):
    def __init__(self, obj):
        self.original_obj = obj
        HttpResponse.__init__(self, self.serialize())
        self["Content-Type"] = "text/javascript"

    def serialize(self):
        return(simplejson.dumps(self.original_obj))

def test(request):
    return render_to_response('test.html', {})

def json(request):
    #content = {
    #    'id':'1',
    #    'name':'test',
    #}
    #return JsonResponse(content)
    print "Subzero POST data:", request.POST
    print "Subzero GET data:", request.GET
    return render_to_response('test.json', {})
