# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from optparse import make_option
from django.core.management import BaseCommand
from django.conf import settings
from blog.models import Blog
from utils.helper import md, parse_meta, At2Section
from blog import const

import os, re

template = [("Title", ""), ("Tags", ""), ("Category", ""), ("Type", const.TYPE_SLIDE)]
pattern = r"[^@]*(@.*)@end"

def smart_print(content):
    print(content.encode("utf-8"))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-c', '--create',
            action="store",
            type="string",
            dest="name",
            help=u"新建slides"
        ),
        make_option('-m', '--make',
            action="store",
            type="string",
            dest="make",
            help=u"编译到DB"
        )
        )

    def gen_posts(self, **kwargs):
        title = kwargs.get("name", "")
        if not title:
            return
        post_root = settings.POST_DIR_ROOT
        base = ""
        for key, value in template:
            if key == "Title":
                base += "%s: %s\n" %(key, title)
            else:
                base += "%s: %s\n" %(key, value)

        path = os.path.join(post_root, "%s.md" %title)
        if os.path.exists(path):
            agree = raw_input('已经存在文件,是否覆盖Y/n \n'.encode("utf-8"))
            if agree != 'Y':
                print("exit")
                return
        file_handler = open(path, "w")
        file_handler.write(base)
        file_handler.close()

        print("Success and exit \n")

    def make(self, **kwargs):
        make_path = kwargs.get("make", "")
        if not make_path:
            smart_print(u"请指定文件名")

        post_root = settings.POST_DIR_ROOT
        path = os.path.join(post_root, "%s.md" %make_path)
        file_handler = open(path, "r")
        text = file_handler.read()
        file_handler.close()

        text = text.decode("utf-8")
        at = At2Section()

        html = md.convert(text)
        metadata = parse_meta(md)

        prog = re.compile(pattern, re.DOTALL)
        match = prog.match(html)
        parsed_html = at.parse(match.group(1))

        metadata['content'] = parsed_html

        title = metadata.get("title", "")
        if not title:
            print("MD文件无title")
            return

        blog = Blog.get_by_unique(title=title)
        if not blog:
            blog = Blog(**metadata)
        else:
            for key, value in metadata.items():
                setattr(blog, key.lower(), value)
        blog.save()
        smart_print("博客: %s,存储成功" %title)

    def handle(self, *args, **options):
        if options['name']:
            self.gen_posts(**options)
        elif options['make']:
            self.make(**options)
        else:
            smart_print("亲, 请仔细看看使用说明")