# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import markdown
from markdown.inlinepatterns import Pattern
from markdown.util import etree

SECTION_PATTERN = r'@([^@]+)@'

class SectionPattern(Pattern):
    def handleMatch(self, m):
        el = etree.Element('section')
        el.text = m.group(2)
        return el

section = SectionPattern(SECTION_PATTERN)

class SectionExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = SectionPattern(SECTION_PATTERN)
        md.inlinePatterns.add('section', pattern, '_begin')

def parse_meta(md):
    meta = md.Meta
    info = {}
    for key, value in meta.items():
        try:
            info[key] = value[0]
        except:
            pass
    return info

def makeExtension(configs=None):
    return SectionExtension(configs=configs)


section_extension = makeExtension()
md = markdown.Markdown(extensions = ['meta', section_extension])

