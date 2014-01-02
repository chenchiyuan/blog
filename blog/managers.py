# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db import models
from blog import const


class PostManager(models.Manager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().filter(type=const.TYPE_BLOG)


class SlideManager(models.Manager):
    def get_query_set(self):
        return super(SlideManager, self).get_query_set().filter(type=const.TYPE_SLIDE)