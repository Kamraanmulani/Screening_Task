import os
import sys
import django

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_api.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

print("=" * 50)
print("Setting up IIT B Chemical Equipment App")
print("=" * 50)
print()

# Apply migrations
print("[1/3] Applying database migrations...")
try:
    call_command('migrate', verbosity=0)
    print("✓ Migrations applied successfully")
except Exception as e:
    print(f"✗ Error applying migrations: {e}")
    sys.exit(1)

print()

# Check/Create superuser
print("[2/3] Setting up superuser...")
User = get_user_model()

if User.objects.filter(is_superuser=True).exists():
    admin = User.objects.filter(is_superuser=True).first()
    print(f"✓ Superuser already exists: {admin.username}")
else:
    try:
        User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
        print("✓ Superuser created: admin / admin123")
    except Exception as e:
        print(f"✗ Error creating superuser: {e}")

print()

# Create test user
print("[3/3] Setting up test user...")
if User.objects.filter(username='testuser').exists():
    print("✓ Test user already exists: testuser")
else:
    try:
        User.objects.create_user('testuser', 'test@test.com', 'test123')
        print("✓ Test user created: testuser / test123")
    except Exception as e:
        print(f"Note: {e}")

print()
print("=" * 50)
print("Setup Complete!")
print("=" * 50)
print()
print("Login credentials:")
print("  Admin User:")
print("    Username: admin")
print("    Password: admin123")
print()
print("  Test User:")
print("    Username: testuser")
print("    Password: test123")
print()
print("Now start the server with:")
print("  python manage.py runserver")
