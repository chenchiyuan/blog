# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.views.generic import TemplateView
from blog.models import Blog


class BlogListView(TemplateView):
    template_name = "blog/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        blogs = Blog.blogs.all()
        context['blogs'] = blogs
        return context


class BlogDetailView(TemplateView):
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        blog = Blog.posts.get(**kwargs)
        context["blog"] = blog
        return context


class SlideDetailView(TemplateView):
    template_name = "blog/slide.html"

    def get_context_data(self, **kwargs):
        context = super(SlideDetailView, self).get_context_data(**kwargs)
        slide = Blog.slides.get(**kwargs)
        context["blog"] = slide
        return context


class AboutView(TemplateView):
    template_name = "blog/about.html"