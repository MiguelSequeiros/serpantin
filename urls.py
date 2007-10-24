from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^registration/login', 'django.contrib.auth.views.login'),
    (r'^registration/logout', 'django.contrib.auth.views.logout'),
    #(r'^registration/register/$', 'serpantin.apps.registration.views.register'),
    #(r'^registration/password_reset/$', 'django.views.registration.passwords.password_reset'),
    #(r'^registration/password_reset/done/$', 'django.views.registration.passwords.password_reset_done'),
    #(r'^registration/password_change/$', 'django.views.registration.passwords.password_change'),
    #(r'^registration/password_change/done/$', 'django.views.registration.passwords.password_change_done'),
#    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/index.html'}),

    #(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'base_dojo.html'}),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'base_dojo09.html'}),
    #(r'^accounts/login', 'django.views.auth.login.login'),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/html/media/', 'show_indexes':True}),

    (r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/save/(?P<object_id>.*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    (r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/save/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    (r'^async/(?P<app_name>.*)/(?P<model_name>.*)/saveandgo/(?P<object_id>.*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form', dict({'go':True})),
    (r'^async/(?P<app_name>.*)/(?P<model_name>.*)/saveandgo/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form', dict({'go':True})),
    (r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),
    (r'^async/(?P<app_name>[a-z]*)/(?P<model_name>[A-Za-z]*)/(?P<object_id>.*)/form/(?P<win_id>.*)/$', 'serpantin.apps.common.views.async_form'),

    (r'^async/(?P<node>.*)/(?P<app_name>.*)/(?P<model_name>.*)/list/$', 'serpantin.apps.common.views.async_listform'),

    # Test urls
    (r'^test/$', 'serpantin.apps.test.views.test'),
    (r'^json/$', 'serpantin.apps.test.views.json'),
)
