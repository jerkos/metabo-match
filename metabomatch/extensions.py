# -*- coding: utf-8 -*-
"""
    flaskbb.extensions
    ~~~~~~~~~~~~~~~~~~~~

    The extensions that are used by FlaskBB.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_redis import Redis
from flask_migrate import Migrate
from flask_themes2 import Themes
from flask_plugins import PluginManager
from flask_github import GitHub
from flask_htmlmin import HTMLMIN
from flask_wtf.csrf import CsrfProtect
from flask_gravatar import Gravatar
from flask_babel import Babel

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Mail
mail = Mail()

# Caching
cache = Cache()

# Redis
redis_store = Redis()

# Debugtoolbar
#debugtoolbar = DebugToolbarExtension()

# Migrations
migrate = Migrate()

# Themes
themes = Themes()

# PluginManager
plugin_manager = PluginManager()

# performing API call to github
github = GitHub()

gravatar = Gravatar(default='identicon')

# csrf protection
csrf = CsrfProtect()

babel = Babel()

compress = Compress()

htmlminify = HTMLMIN()