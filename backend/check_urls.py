from django.core.management import setup_environ
import sys
sys.path.insert(0, 'C:\\Users\\Kamraam\\Desktop\\Github Repo\\IIT B\\backend')

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_api.settings')
django.setup()

from rest_framework.routers import DefaultRouter
from api.views import DatasetViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

print("Registered URLs:")
for pattern in router.urls:
    print(f"  {pattern.pattern} -> {pattern.name}")
