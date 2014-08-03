# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db import models
from blog import const
from blog.managers import PostManager, SlideManager
from blog.mixin import QueryMixin
from django.utils import timezone
from utils.slugify import slugify
from bs4 import BeautifulSoup


class Blog(models.Model, QueryMixin):
    class Meta:
        app_label = 'blog'
        db_table = 'blog_blog'
        verbose_name = verbose_name_plural = u"博客"
        ordering = ['-modify_at']

    slug = models.CharField(u"slug", max_length=const.DB_TITLE_LENGTH, unique=True, null=True)
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

    objects = models.Manager()
    blogs = models.Manager()
    posts = PostManager()
    slides = SlideManager()

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        return super(Blog, self).save(force_insert, force_update, using, update_fields)

    @property
    def snapshot(self):
        if not self.type:
            soup = BeautifulSoup(self.content)
            try:
                return soup.find("p").text
            except:
                return self.content[:100]
        else:
            return '<iframe src="%s" style="margin-top:21px;margin-bottom:10.5px"></iframe>' % self.absolute_url

    @property
    def absolute_url(self):
        if not self.type:
            url = "/posts/%s/" % self.slug
        else:
            url = "/slides/%s/" % self.slug
        return url
