#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import subprocess
import os
import base64
from pelican import signals

cur_dir = os.path.dirname(os.path.abspath(__file__))

def typo(article_generator):
    for article in article_generator.articles:
        base64_content = base64.b64encode(article._content.encode('utf-8'))
        cmd = "php {0}/typograf.php {1}".format(cur_dir, base64_content)
        typograf = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        article._content = unicode(typograf.stdout.read(), 'utf-8')

def register():
    signals.article_generator_finalized.connect(typo)