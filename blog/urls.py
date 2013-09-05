# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf.urls import patterns, url
from blog import const
from blog import views

urlpatterns = patterns('',
    url(r'^posts/$', views.BlogListView.as_view(), name="blogs"),
    url(r'^posts/%s/$' %const.URL_ID, views.BlogDetailView.as_view(), name="blog_detail"),
)
