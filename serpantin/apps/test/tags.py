from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.newforms import form_for_model, form_for_instance
from django.shortcuts import render_to_response, get_object_or_404

from serpantin.apps.test.models import Article

def article_form(request, object_id=''):
    print "article POST data:\n", request.POST
    if object_id:
        object = get_object_or_404(Article, pk=object_id)
        Form = form_for_instance(object)
    else: Form = form_for_model(Article)
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid(): form.save()
        else:
            errors = form.errors
            return render_to_response('errors.html', {'errors': errors})
        object_url = object_id and object_id or 'new'
        return HttpResponseRedirect('/test/articles/%s/' % object_url)
    else:
        form = Form()
        params = {
            'form': form,
            'object_id': object_id,
        }
        template_name = 'tags/article_form.html'
        return render_to_response(template_name, params, context_instance=RequestContext(request))
