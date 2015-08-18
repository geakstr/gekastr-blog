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

DEFAULT_PAGINATION = 2
DEFAULT_ORPHANS = 0
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

DATE_FORMATS = {
    'en': ('en_US', '%B %-d, %Y'),
    'ru': ('ru_RU', '%-d %B %Y'),
}

PATH = '../content'
OUTPUT_PATH = '../output'
ARTICLE_PATHS = ['./articles']
PAGE_PATHS = ['./pages']
STATIC_PATHS = ['images']
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


ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_LANG_URL = '{slug}-{lang}'
ARTICLE_LANG_SAVE_AS = '{slug}-{lang}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORYS_SAVE_AS = ''