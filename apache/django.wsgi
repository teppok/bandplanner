import os
import sys

path = '/home/teppo/django'
if path not in sys.path:
    sys.path.append(path)
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'bandplanner.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

