"""
WSGI config for smartsuite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsuite.settings')

import os
from dotenv import load_dotenv

smartsuite_folder = os.path.join(os.getcwd(), 'smartsuite')  # or use os.path.abspath('smartsuite')
load_dotenv(os.path.join(smartsuite_folder, '.env'))

application = get_wsgi_application()

app = application
