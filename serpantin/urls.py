from django.conf import settings
from django.conf.urls.defaults import *
#for newforms-admin
from django.contrib import admin

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    #newforms-admin
    #(r'^admin/(.*)', admin.site.root),

    (r'^accounts/login', 'django.contrib.auth.views.login'),
    (r'^accounts/logout', 'django.contrib.auth.views.logout'),
    #(r'^registration/register/$', 'serpantin.apps.registration.views.register'),
    #(r'^registration/password_reset/$', 'django.views.registration.passwords.password_reset'),
    #(r'^registration/password_reset/done/$', 'django.views.registration.passwords.password_reset_done'),
    #(r'^registration/password_change/$', 'django.views.registration.passwords.password_change'),
    #(r'^registration/password_change/done/$', 'django.views.registration.passwords.password_change_done'),
#    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/index.html'}),

    (r'^$', 'serpantin.apps.common.views.direct_to_template_auth', {'template': 'base_dojo.html'}),
    #(r'^accounts/login', 'django.views.auth.login.login'),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/html/media/', 'show_indexes':True}),

    #(r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/save/(?P<object_id>.*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    #(r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/save/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    #(r'^async/(?P<app_name>.*)/(?P<model_name>.*)/saveandgo/(?P<object_id>.*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form', dict({'go':True})),
    #(r'^async/(?P<app_name>.*)/(?P<model_name>.*)/saveandgo/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form', dict({'go':True})),
    #(r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    #(r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/(?P<object_id>.*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    
    # async
    #(r'^async/(?P<node>.*)/(?P<app_name>.*)/(?P<model_name>.*)/list/$', 'serpantin.apps.common.views.async_listform'),
    
    (r'^async/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/$', 'serpantin.apps.common.views.async_list'),
    (r'^async/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/new/(?P<win_id>.+)/$', 'serpantin.apps.common.views.async_form'),
    (r'^async/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/(?P<object_id>.+)/delete/$', 'serpantin.apps.common.views.async_delete'),
    (r'^async/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/(?P<object_id>.+)/(?P<win_id>.+)/$', 'serpantin.apps.common.views.async_form'),
    
    (r'^json/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/$', 'serpantin.apps.common.views.json'),
    # Test urls
    (r'^test/$', 'serpantin.apps.test.views.test'),
    (r'^test/article/new/$', 'serpantin.apps.test.tags.article_form'),
    (r'^test/article/(?P<object_id>.+)/$', 'serpantin.apps.test.tags.article_form'),
    #(r'^json/$', 'serpantin.apps.test.views.json'),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns('',
        (r'^site_media/dojo/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DOJO_DIR, 'show_indexes':True}),
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
