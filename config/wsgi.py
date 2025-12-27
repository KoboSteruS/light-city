"""
WSGI config для проекта Яркий Город.

Используется для развертывания проекта на production серверах.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()

