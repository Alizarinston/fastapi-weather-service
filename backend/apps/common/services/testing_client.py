from contextlib import contextmanager
from typing import Dict

from fastapi import FastAPI
from httpx import AsyncClient


class TestClient:
    base_url = 'http://test'

    def __init__(self, app: FastAPI):
        self.app = app
        self.headers: Dict[str, str] = {}

    @contextmanager
    def force_client_auth(self):
        # TODO:
        yield

    async def get(self, *args, **kwargs):
        async with AsyncClient(app=self.app, base_url=self.base_url) as async_client:
            headers = kwargs.pop('headers', {})
            headers.update(self.headers)

            return await async_client.get(*args, headers=headers, **kwargs)

    async def post(self, *args, **kwargs):
        async with AsyncClient(app=self.app, base_url=self.base_url) as async_client:
            headers = kwargs.pop('headers', {})
            headers.update(self.headers)

            return await async_client.post(*args, headers=headers, **kwargs)

    async def put(self, *args, **kwargs):
        async with AsyncClient(app=self.app, base_url=self.base_url) as async_client:
            headers = kwargs.pop('headers', {})
            headers.update(self.headers)

            return await async_client.put(*args, headers=headers, **kwargs)

    async def delete(self, *args, **kwargs):
        async with AsyncClient(app=self.app, base_url=self.base_url) as async_client:
            headers = kwargs.pop('headers', {})
            headers.update(self.headers)

            return await async_client.delete(*args, headers=headers, **kwargs)
