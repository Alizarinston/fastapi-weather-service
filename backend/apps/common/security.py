import json
from typing import Any

from cryptography.fernet import Fernet

__encoding = 'utf-8'


def encrypt(data: Any):
    from config.main import settings

    payload = json.dumps(data)
    fernet = Fernet(settings.SECRET_KEY.get_secret_value().encode(__encoding))

    return fernet.encrypt(payload.encode(__encoding))


def decrypt(data: str):
    from config.main import settings

    fernet = Fernet(settings.SECRET_KEY.get_secret_value().encode(__encoding))
    payload = fernet.decrypt(data.encode(__encoding))

    return json.loads(payload.decode(__encoding))
