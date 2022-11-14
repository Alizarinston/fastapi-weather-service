from importlib import import_module


def get_model_modules():
    from config.main import settings

    model_modules: list[str] = []

    for app_module in settings.INSTALLED_APPS:
        models_path = f'{getattr(app_module, "__package__")}.models'

        try:
            import_module(models_path)
        except ImportError:
            continue

        model_modules.append(models_path)

    return model_modules
