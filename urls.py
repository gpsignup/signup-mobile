from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'signup.views.index'),
    url(r'^create/$', 'signup.views.create'),
    url(r'^results/(?P<event_id>\d+)/$', 'signup.views.results'),
    url(r'^view/(?P<event_id>\d+)/$', 'signup.views.view'),
    url(r'^manage/$', 'signup.views.manage'),
    url(r'^signup/$', 'signup.views.signup'),
    url(r'^thanks/$', 'signup.views.thanks'),
)
