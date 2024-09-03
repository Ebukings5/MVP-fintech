"""
WSGI config for finance_manager project.

This module contains the WSGI application used by Django's runserver and
any WSGI-compatible web server. It exposes the WSGI callable as a module-level
variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'DJANGO_SETTINGS_MODULE' environment variable.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')

# Get the WSGI application for the project.
application = get_wsgi_application()