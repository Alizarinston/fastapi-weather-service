from apps.models import get_model_modules
from config.main import settings

TORTOISE_ORM = {
    'connections': {'default': settings.DATABASE_URL},
    'apps': {
        'models': {
            'models': get_model_modules(),
            'default_connection': 'default',
        },
    },
}
