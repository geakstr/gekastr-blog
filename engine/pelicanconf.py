#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

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

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 3
PAGINATION_PATTERNS = (
    (1, '{base_name}/{name}', 'blog/{name}.html'),
    (2, '{base_name}/{name}/page/{number}', 'blog/{name}/page/{number}/index.html'),
)

DATE_FORMATS = {
    'en': ('en_US', '%B %-d, %Y'),
    'ru': ('ru_RU', '%-d %B %Y'),
}

PATH = '../content'
OUTPUT_PATH = '../output'
ARTICLE_PATHS = ['./articles']
PAGE_PATHS = ['./pages']
STATIC_PATHS = ['imgs', 'pdfs']
OUTPUT_RETENTION = [".git", ".gitignore"]

CURRENT_YEAR = datetime.datetime.utcnow().strftime("%Y")

DIRECT_TEMPLATES = ['index']
PAGINATED_DIRECT_TEMPLATES = ['index']

THEME = './theme'
THEME_STATIC_PATHS = ['static']
CSS_FILE = 'style.css'
TYPOGRIFY = False

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


ARTICLE_URL = 'blog/{slug}'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
ARTICLE_LANG_URL = 'blog/{slug}-{lang}'
ARTICLE_LANG_SAVE_AS = 'blog/{slug}-{lang}.html'

TAG_URL = 'blog/tags/{slug}'
TAG_SAVE_AS = 'tags/{slug}.html'

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORYS_SAVE_AS = ''