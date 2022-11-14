import logging

from config.constants import TESTING_ENVIRONMENT
from config.main import settings


class RequireTestingEnvironmentFalse(logging.Filter):
    def filter(self, record):
        return settings.ENVIRONMENT != TESTING_ENVIRONMENT
