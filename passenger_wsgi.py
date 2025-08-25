import os
import sys
import logging
logging.basicConfig(filename='/home/anuragroup/logs/django_passenger.log', level=logging.DEBUG)

project_root = "/home/anuragroup/public_html/agcresourceportal.net/anuacc"
sys.path.insert(0, project_root)
venv_path = "/home/anuragroup/virtualenv/public_html/agcresourceportal.net/anuacc/3.11/lib64/python3.11/site-packages"
sys.path.insert(0, venv_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "import_system.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

