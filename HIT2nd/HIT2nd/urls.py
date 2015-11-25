# -*- coding: utf-8 -*-
from django.conf.urls import *
from HSTP.views import *
import settings
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
    url('^logout/$',logout),
    url('^my_product/$',my_product),
    url('^delete_product/$',delete_product),
    url('^finish_user/$',finish_user),
    url('^search_product/$',search_product),
    url('^index/$',index),
    url('^$',return_index),
    url('^return_index2/$',return_index2),
    url('^add_product/$',add_product),
#    url(r'^static/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url('^product_show/$',product_show),
    url('^seller_inf/$',seller_inf),
    url('^user_inf/$',user_inf),
    
      
)
