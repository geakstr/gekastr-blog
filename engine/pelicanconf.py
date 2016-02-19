#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'Дмитрий Харитонов'
SITENAME = u'Forkbomb Blog'
SITEURL = 'http://dkharitonov.me'
TIMEZONE = 'Europe/Moscow'
DEFAULT_LANG = u'ru_RU'

USE_FOLDER_AS_CATEGORY = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = True
SLUGIFY_SOURCE = 'title'

DEFAULT_PAGINATION = 5
DEFAULT_ORPHANS = 0
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
STATIC_PATHS = ['imgs', 'pdfs', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

CURRENT_YEAR = datetime.datetime.utcnow().strftime("%Y")

DIRECT_TEMPLATES = ['index']
PAGINATED_DIRECT_TEMPLATES = ['index']

THEME = './theme'
THEME_STATIC_PATHS = ['static']
CSS_FILE = 'style.css'

import md5
def my_slugify(value, sep):
    m = md5.new()
    m.update(value.encode("UTF-8"))
    return "toc_{}".format(m.digest().encode("hex"))
from markdown.extensions.headerid import HeaderIdExtension

MD_EXTENSIONS = ['extra', 'codehilite', 'toc', HeaderIdExtension(configs=[('slugify', my_slugify)])]

PLUGIN_PATHS = ["plugins"]
PLUGINS = ['assets', 'readtime', 'typo', 'share_post']

FEED_DOMAIN = SITEURL
FEED_RSS =  'feeds/rss.xml'
FEED_ATOM =  None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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

MD_INLINE = {}



ASSET_CACHE = False
ASSET_DEBUG = False