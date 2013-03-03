import os
import sys

dirname = os.path.dirname
PROJECT_PATH = os.path.realpath(dirname(dirname(__file__)))

if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto_pizarras.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
