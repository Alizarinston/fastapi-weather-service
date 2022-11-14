"""isort:skip_file"""

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from apps.common.middlewares.utils import init_middlewares
from apps.database import init_database
from apps.error_handlers import http_exception_handler
from apps.error_handlers import python_exception_handler
from apps.error_handlers import validation_exception_handler
from apps.router import init_routers
from config.main import settings

app = FastAPI(
    debug=False,
    title=settings.PROJECT_NAME,
)

# init error handlers
app.add_exception_handler(Exception, python_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

init_routers(app)
init_middlewares(app)
init_database(app)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=settings.LOGGING)  # nosec
