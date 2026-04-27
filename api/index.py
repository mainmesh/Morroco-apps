import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morocco_loans.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
