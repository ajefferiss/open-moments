#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Adam Jefferiss'
SITENAME = u'Open-Moments'
SITESUBTITLE = u''
SITEURL = ''
TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

DEFAULT_PAGINATION = 3

THEME = 'themes/bootstrap-brew'

PATH = 'content'
PAGE_PATHS = ['pages']

PYGMENTS_STYLE = 'monokai'
MARKDOWN = {'extensions': [
                            'toc',
                            'fenced_code',
                            'codehilite(css_class=highlight)',
                          ]}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True

SOCIAL = (
    ('github', 'https://github.com/ajefferiss'),
    ('twitter', 'https://twitter.com/adamjefferiss'),
    ('linkedin', 'https://www.linkedin.com/in/adam-jefferiss-b4567256/'),
    ('google+', 'https://plus.google.com/+AdamJefferiss'),
    ('stack overflow', 'https://stackoverflow.com/users/1823022/ajefferiss'),
 )

# Cleaner page links
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_LANG_URL = '{slug}-{lang}.html'
PAGE_LANG_SAVE_AS = '{slug}-{lang}.html'

# Cleaner Articles
ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISQUS_SITENAME = 'open-moments'

FAVICON = 'theme/images/favicon.png'
FAVICON_IE = 'theme/images/favicon-32x32.png'
TOUCHICON = 'theme/images/favicon-touch.png'
