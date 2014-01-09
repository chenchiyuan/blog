# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import markdown
from bs4 import BeautifulSoup


class HtmlFormatter(object):
    @classmethod
    def format_html(self, html):
        html = self.format_table(html)
        return html

    @classmethod
    def format_table(cls, html):
        soup = BeautifulSoup(html)
        tables = soup.find_all("table")
        for table in tables:
            table.attrs['class'] = table.attrs.get("class", "") + "table table-striped table-responsive"
        return unicode(soup)


def parse_meta(md):
    meta = md.Meta
    info = {}
    for key, value in meta.items():
        try:
            info[key] = value[0]
        except:
            pass
    return info

class At2Section(object):
    def __init__(self):
        self.stack = []

    def pop(self):
        self.stack.pop(index=-1)

    def push(self, item):
        self.stack.append(item)

    def parse(self, text):
        at = ""
        buffer = ""

        for item in text:
            if not item == "@":
                if at:
                    self.push(buffer)
                    self.push(at)
                    at = ""
                    buffer = ""
                buffer += item
            else:
                at += "@"
        self.push(buffer)
        return self.to_text()

    def to_text(self):
        current = ""
        text = ""
        for item in self.stack:
            if not item:
                continue
            elif item[0] == "@":
                if len(item) > len(current):
                    text += "<section>" * (len(item) - len(current))
                elif len(item) == len(current):
                    text += "</section><section>"
                else:
                    text += "</section>" * (len(current) - len(item))
                    text += "</section><section>"
                current = item
            else:

                text += item.strip()

        text += "</section>" *len(current)
        return text


md = markdown.Markdown(extensions=['meta', 'tables'])

