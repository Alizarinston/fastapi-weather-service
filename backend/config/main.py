import importlib
import logging.config
import sys

from config.constants import DEVELOPMENT_ENVIRONMENT, TESTING_ENVIRONMENT
from pydantic import BaseSettings, PostgresDsn, SecretStr, validator


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    PROJECT_NAME = ''
    OWM_API_KEY: str = ''
    DEBUG = True
    ENVIRONMENT = DEVELOPMENT_ENVIRONMENT

    BACKEND_BASE_URL: str = ''

    @validator('ENVIRONMENT')
    def force_testing_environment(cls, value: str | None) -> str:
        if cls.is_test():
            return TESTING_ENVIRONMENT
        return str(value)

    # generate it by python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
    SECRET_KEY: SecretStr = SecretStr('wHrekwqeEi6NF3pTPorWZ97lTXdegJRSz1hiaEn9rhQ=')

    INSTALLED_APPS: list[str] = [
        'apps.common',
        'apps.accounts',
        'apps.zip_weather',
        'aerich',
    ]

    MIDDLEWARES: list[str | tuple[str, dict]] = [
        (
            'starlette.middleware.cors.CORSMiddleware',
            {
                'allow_origins': ['*'],
                'allow_methods': ['*'],
                'allow_headers': ['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token'],
            },
        ),
    ]

    @validator('INSTALLED_APPS')
    def load_installed_apps(cls, values: list[str]) -> list:
        return [importlib.import_module(module) for module in values]

    @staticmethod
    def is_test():
        cmd = sys.argv[0] if sys.argv else ''
        return 'pytest' in cmd

    LOGGING_FORMAT: str = '%(levelname)-8s %(message)s (%(pathname)s:%(lineno)d) %(name)s.%(funcName)s'
    LOGGING_ROOT_LOG_LEVEL: str = 'WARNING'
    LOGGING_WEB_SERVER_LEVEL: str = 'INFO'
    LOGGING_APP_LOG_LEVEL: str = 'INFO'
    LOGGING_HANDLERS: list[str] = ['default']

    LOGGING: dict = {}

    @validator('LOGGING')
    def set_logger_config(cls, value: dict, values: dict):
        if not value:
            value = {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'default': {
                        'format': values['LOGGING_FORMAT'],
                        'style': '%',
                        'use_colors': True,
                    },
                    'json': {
                        'format': '%(message)s',
                        'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                    },
                },
                'filters': {
                    'require_tests_false': {
                        '()': 'apps.common.log_filters.RequireTestingEnvironmentFalse',
                    },
                },
                'handlers': {
                    'default': {
                        'class': 'logging.StreamHandler',
                        'filters': ['require_tests_false'],
                        'level': values['LOGGING_APP_LOG_LEVEL'],
                        'formatter': 'default',
                    },
                    'json': {
                        'class': 'logging.StreamHandler',
                        'filters': ['require_tests_false'],
                        'level': values['LOGGING_APP_LOG_LEVEL'],
                        'formatter': 'json',
                    },
                    'null': {
                        'class': 'logging.NullHandler',
                    },
                },
                'loggers': {
                    'uvicorn': {
                        'level': values['LOGGING_WEB_SERVER_LEVEL'],
                        'propagate': False,
                    },
                    'uvicorn.access': {
                        'level': values['LOGGING_WEB_SERVER_LEVEL'],
                        'propagate': False,
                        'handlers': ['null'],
                    },
                    'fastapi': {
                        'level': values['LOGGING_WEB_SERVER_LEVEL'],
                        'propagate': False,
                    },
                    # app logger
                    'apps': {
                        'level': values['LOGGING_APP_LOG_LEVEL'],
                        'propagate': True,
                    },
                },
            }

        for logger in value['loggers'].values():
            if 'handlers' not in logger:
                logger['handlers'] = values['LOGGING_HANDLERS']
        return value

    # Postgresql
    DATABASE_URL: PostgresDsn

    @validator('DATABASE_URL')
    def force_testing_database(cls, value: PostgresDsn) -> str:
        assert value.path and len(value.path) > 1, 'database must be provided'

        if cls.is_test():
            return PostgresDsn.build(
                scheme=value.scheme,
                user=value.user,
                password=value.password,
                host=value.host,
                port=value.port,
                path='/test_db',
                query=value.query,
                fragment=value.fragment,
            )
        return value


settings = Settings()
logging.config.dictConfig(settings.LOGGING)
