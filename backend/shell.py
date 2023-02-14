import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from forum.models import *
from django.contrib.auth import get_user_model

# exec(open('shell.py', 'r').read())

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())