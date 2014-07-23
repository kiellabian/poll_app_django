from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url('', include('polls.urls', namespace='polls')),
	url(r'^poll/', include('polls.urls', namespace='polls')),
    url(r'^admin/', include(admin.site.urls)),
)
