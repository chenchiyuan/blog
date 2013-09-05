# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from optparse import make_option
from django.core.management import BaseCommand
from django.conf import settings
from collections import OrderedDict
import os

template = [("Title", ""), ("Tags", ""), ("Category", "")]

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-c', '--create',
            action="store",
            type="string",
            dest="name",
            help=u"新建blog"
        ),
        make_option('-m', '--make',
            action="store_true",
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
                base += "%s: \n" %key

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
        return

    def handle(self, *args, **options):
        if options['name']:
            self.gen_posts(**options)
        elif options['make']:
            self.make(**options)
