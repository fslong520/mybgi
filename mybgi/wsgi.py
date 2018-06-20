"""
WSGI config for mybgi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import os
import sys
from os.path import abspath, dirname, join

PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "mybgi.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()