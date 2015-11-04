# -*- coding: utf-8 -*-
from django.conf.urls import *
from HSTP.views import *
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
admin.autodiscover()
urlpatterns = patterns('',
                       
    url(r'^admin/', include(admin.site.urls)),
    url('^register/$',register),
    url('^return_login/$',return_login),
	url('^login/$',login),
    url('^finish_user/$',finish_user),
    

   
)
