import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

logger = logging.getLogger('apps')


def init_database(app: FastAPI):
    from config.main import settings
    from config.orm import TORTOISE_ORM

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=settings.is_test(),
    )
