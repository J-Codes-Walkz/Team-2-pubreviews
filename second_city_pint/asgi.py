import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "second_city_pint.settings")

application = get_asgi_application()
