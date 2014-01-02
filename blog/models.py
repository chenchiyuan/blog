# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db import models
from blog import const
from blog.managers import PostManager, SlideManager
from blog.mixin import QueryMixin
from django.utils import timezone


class Blog(models.Model, QueryMixin):
    class Meta:
        app_label = 'blog'
        db_table = 'blog_blog'
        verbose_name = verbose_name_plural = u"博客"

    title = models.CharField(u"标题", max_length=const.DB_TITLE_LENGTH, blank=True, null=True)
    content = models.TextField(u"内容", max_length=const.DB_CONTENT_LENGTH, blank=True, null=True,
        help_text="Markdown text")

    category = models.CharField(u"分类", max_length=const.DB_NAME_LENGTH, blank=True, null=True)
    tags = models.CharField(u"标签", max_length=const.DB_NAME_LENGTH, blank=True, null=True)

    type = models.SmallIntegerField(u"类型", choices=const.TYPE_CHOICES,
        default=const.TYPE_BLOG, blank=True, null=True)

    short_description = models.TextField(u"简要介绍", max_length=const.DB_CONTENT_LENGTH,
                                         default="", blank=True, null=True)

    created_at = models.DateTimeField(u"创建于", blank=True, null=True, default=timezone.now)
    modify_at = models.DateTimeField(u"修改于", blank=True, null=True, default=timezone.now, auto_now=True)

    blogs = models.Manager()
    posts = PostManager()
    slides = SlideManager()

    def __unicode__(self):
        return self.title

    @property
    def snapshot(self):
        return self.content[:100]