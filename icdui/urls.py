from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'icdui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('web.urls')), #this is to route "/" to "/web". Need to route /web/* to /*
    url(r'^admin/', include(admin.site.urls)),
    url(r'^web/', include('web.urls')), # ADD THIS NEW TUPLE!
    #url(r'', include(django_u2f.urls)), #this is to route "/" to "/web". Need to route /web/* to /*


)
