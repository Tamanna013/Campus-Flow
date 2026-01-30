import os
from django.core.asgi import get_asgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# This handles standard HTTP requests (Login, Register, Bookings, etc.)
application = get_asgi_application()