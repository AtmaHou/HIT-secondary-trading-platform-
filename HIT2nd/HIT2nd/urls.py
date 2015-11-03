from django.conf.urls import *

from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
admin.autodiscover()
urlpatterns = patterns('',
                       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',  'HSTP.views.login'),
    url(r'^logout/$', 'HSTP.views.logout'),
    url(r'^register/$','HSTP.views.register'),
    
    # Examples:
    # url(r'^$', 'HIT2nd.views.home', name='home'),
    # url(r'^HIT2nd/', include('HIT2nd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
