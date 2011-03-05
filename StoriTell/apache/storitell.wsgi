import os, sys
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
 
sys.path.insert(0,'/usr/lib/python2.6/site-packages/django/')
sys.path.insert(0,'/home/django/public_html/storitell.com/storitell')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'storitell.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
