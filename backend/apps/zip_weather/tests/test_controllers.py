import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_weather_info_api_success(client):
    response = await client.get(client.app.url_path_for('weather_info', zip_code='12345'))

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_weather_info_api_fails_too_many_characters(client):
    response = await client.get(client.app.url_path_for('weather_info', zip_code='123456'))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == [
        {
            'loc': ['path', 'zip_code'],
            'msg': 'ensure this value has at most 5 characters',
            'type': 'value_error.any_str.max_length',
            'ctx': {'limit_value': 5},
        }
    ]
