"""isort:skip_file"""

import logging

from fastapi.exception_handlers import http_exception_handler as fastapi_http_exception_handler
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger('apps')


async def python_exception_handler(request, exc):
    logger.warning(
        f'Uncaught exception: {exc}',
        exc_info=exc,
        extra={
            'type': 'python_exception',
            'endpoint': request.url.path,
            'method': request.method,
        },
    )

    return JSONResponse({'detail': str(exc)}, status_code=500)


async def validation_exception_handler(request, exc):
    logger.warning(
        f'Invalid schema: {request.url.path}',
        exc_info=exc,
        extra={
            'type': 'http_validation_error',
            'endpoint': request.url.path,
            'method': request.method,
        },
    )

    return await request_validation_exception_handler(request, exc)


async def http_exception_handler(request, exc: HTTPException):
    logger.warning(
        f'Caught exception: {exc}',
        exc_info=exc,
        extra={
            'type': 'http_exception',
            'endpoint': request.url.path,
            'method': request.method,
        },
    )

    return await fastapi_http_exception_handler(request, exc)
