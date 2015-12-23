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
	url('^my_collection/$',my_collection),
    url('^delete_product/$',delete_product),
    url('^finish_user/$',finish_user),
    url('^search_product/$',search_product),
    url('^index/$',index),
    url('^$',index),
    url('^add_product/$',add_product),
#    url(r'^static/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url('^product_show/$',product_show),
    url('^seller_inf/$',seller_inf),
    url('^user_inf/$',user_inf),
    url('^remove_collection/$',remove_collection),
    url('^check_email/$',check_email),
    url('^activate_email/$',activate_email),
    url('^map/$',show_map),
    url('^auction/$',auction),
    url('^bargain/$',bargain),
    url('^all_message/$',all_message),
    url('^add_want/$',add_want),
    url('^want_show/$',want_show),
      
)
