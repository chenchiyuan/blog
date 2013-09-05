# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import markdown

def parse_meta(md):
    meta = md.Meta
    info = {}
    for key, value in meta.items():
        try:
            info[key] = value[0]
        except:
            pass
    return info

md = markdown.Markdown(extensions = ['meta'])