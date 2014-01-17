# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

# DB
DB_NAME_LENGTH = 64
DB_TITLE_LENGTH = 128
DB_CONTENT_LENGTH = 16384

TYPE_BLOG = 0
TYPE_SLIDE = 1

TYPE_CHOICES = (
    (TYPE_BLOG, "博客"),
    (TYPE_SLIDE, "幻灯片")
)

# URLS
URL_ID = "(?P<id>[0-9]+)"
URL_BLOG_ID = "(?P<blog_id>[0-9]+)"
URL_SLUG = "(?P<slug>[a-zA-Z0-9-]+)"


