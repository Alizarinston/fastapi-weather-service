import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Environment
TESTING_ENVIRONMENT = 'testing'
DEVELOPMENT_ENVIRONMENT = 'development'
STAGING_ENVIRONMENT = 'staging'
PRODUCTION_ENVIRONMENT = 'production'

# API Tags
TAG_COMMON = 'Common'
TAG_ACCOUNTS = 'Accounts'
TAG_ZIP_WEATHER = 'Zip Weather'


def get_default_environment():
    if 'test' in sys.argv:
        return TESTING_ENVIRONMENT
    return DEVELOPMENT_ENVIRONMENT
