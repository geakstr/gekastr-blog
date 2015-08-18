#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Дмитрий Харитонов'
SITENAME = u'Дмитрий Харитонов'
SITESUBTITLE = u'Блог'
SITEURL = ''
TIMEZONE = 'Europe/Moscow'
DEFAULT_LANG = u'ru'

USE_FOLDER_AS_CATEGORY = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = True
SLUGIFY_SOURCE = 'title'

DEFAULT_PAGINATION = 15
DEFAULT_ORPHANS = 5

DATE_FORMATS = {
    'en': ('en_US', '%a, %d %b %Y'),
    'ru': ('ru_RU', '%d %B %Y'),
}

PATH = '../content'
OUTPUT_PATH = '../output'
ARTICLE_PATHS = ['./articles']
PAGE_PATHS = ['./pages']
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
OUTPUT_RETENTION = [".git", ".gitignore"]

THEME = './theme'
TYPOGRIFY = True

MD_EXTENSIONS = ['extra']

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["slugcollision"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),)


ARTICLE_URL = '{slug}.html'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_LANG_URL = '{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = '{slug}-{lang}.html'

TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'