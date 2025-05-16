import os
from django.core.wsgi import get_wsgi_application

# Establecer el entorno de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfil_profesional.settings')

# Crear la aplicación WSGI
application = get_wsgi_application()
