# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.views.generic import TemplateView
from blog.models import Blog

class BlogListView(TemplateView):
    template_name = "blog/blogs.html"

class BlogDetailView(TemplateView):
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        super_context = super(BlogDetailView, self).get_context_data(**kwargs)
        blog = Blog.get_by_unique(**kwargs)
        super_context["blog"] = blog
        return super_context

class SlideDetailView(TemplateView):
    template_name = "blog/slide.html"

    def get_context_data(self, **kwargs):
        super_context = super(SlideDetailView, self).get_context_data(**kwargs)
        blog = Blog.get_by_unique(**kwargs)
        super_context["blog"] = blog
        return super_context