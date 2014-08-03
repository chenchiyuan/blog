# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

import unicodedata
from pypinyin import lazy_pinyin

try:
    from django.utils.encoding import smart_unicode as smart_text
except ImportError:
    from django.utils.encoding import smart_text


def slugify(s):
    # L and N signify letter/number.
    # http://www.unicode.org/reports/tr44/tr44-4.html#GC_Values_Table
    rv = []
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYS0123456789"
    stack = ""
    for c in unicodedata.normalize('NFKC', smart_text(s)):
        if c in letters:
            stack += c
            continue

        if stack:
            rv.append(stack)
        stack = ""

        cat = unicodedata.category(c)[0]
        if cat in 'L':
            rv.extend(lazy_pinyin(c))
    new = '-'.join(rv).strip()
    if not new:
        return s
    return new