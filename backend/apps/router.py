import importlib
import pkgutil
from importlib import import_module
from types import ModuleType

from fastapi import APIRouter
from fastapi import FastAPI

router = APIRouter()


def init_routers(app: FastAPI):
    from config.main import settings

    for app_module in settings.INSTALLED_APPS:
        router_path = f'{getattr(app_module, "__package__")}.router'

        try:
            app_router = import_module(router_path)
        except ImportError:
            continue

        if hasattr(app_router, 'router'):
            load_controllers(getattr(app_module, '__package__'))
            app.include_router(getattr(app_router, 'router'))


def load_controllers(package):
    try:
        views: ModuleType = import_module(f'{package}.controllers')
    except ImportError:
        return

    if views.__package__ and not views.__package__ == package:
        import_submodules(views.__package__)


def import_submodules(package_str: str, recursive=True):
    package: ModuleType = importlib.import_module(package_str)

    for loader, name, is_pkg in pkgutil.walk_packages(getattr(package, '__path__')):
        full_name = getattr(package, '__name__') + '.' + name

        importlib.import_module(full_name)

        if recursive and is_pkg:
            import_submodules(full_name)
