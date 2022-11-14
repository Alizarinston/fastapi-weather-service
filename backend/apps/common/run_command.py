import asyncio
import importlib
import logging
import sys
from typing import Callable
from typing import Optional


def run_command(module):
    from apps.app import app
    from apps.app import settings

    cmd_function: Callable = getattr(module, 'command')
    parse_args: Optional[Callable] = getattr(module, 'parse_args', None)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    if parse_args:
        parsed_args = parse_args()
        loop.run_until_complete(cmd_function(settings, app, parsed_args))
    else:
        loop.run_until_complete(cmd_function(settings, app))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error(
            'You need to provide command. Example: python -m apps.common.run_command accounts.create_admin_user',
        )
        exit(0)

    cmd = sys.argv[1]

    app_name, command_path = cmd.split('.', 1)

    module = importlib.import_module(f'apps.{app_name}.commands.{command_path}')

    run_command(module)
