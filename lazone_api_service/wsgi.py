"""
WSGI config for lazone_api_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""


import os
from dotenv import load_dotenv

# Loading environment variables from .env
load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lazone_api_service.settings')

application = get_wsgi_application()
