from typing import List

from apps.accounts.models import User
from apps.accounts.utils import get_current_user
from apps.common.serializers import Status
from apps.zip_weather.models import ZipCode
from apps.zip_weather.router import router
from apps.zip_weather.serializers.weather_result import FavouriteZipCodeResult
from apps.zip_weather.serializers.weather_result import WeatherResult
from config.main import settings
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from pyowm import OWM
from tortoise.contrib.fastapi import HTTPNotFoundError

owm = OWM(settings.OWM_API_KEY)


@router.get('/weather_info/{zip_code}', response_model=WeatherResult)
async def weather_info(zip_code: str = Path(max_length=5)) -> Response:
    mgr = owm.weather_manager()
    result_observation = mgr.weather_at_zip_code(zip_code, country='us')
    result_weather = result_observation.weather

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'zip_code': zip_code,
            'detailed_status': result_weather.detailed_status,
            'temperature': result_weather.temperature('celsius')['temp'],
            'wind_speed': result_weather.wnd['speed'],
            'pressure': result_weather.pressure['press'],
            'humidity': result_weather.humidity,
            'location_name': result_observation.location.name,
        },
    )


@router.get('/favourite_zip_codes', response_model=List[FavouriteZipCodeResult], status_code=status.HTTP_200_OK)
async def read_favourite_zip_codes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    search: str | None = None,
):
    zip_codes = ZipCode.filter(users__id=current_user.id)
    if search:
        zip_codes = zip_codes.filter(code__startswith=search)

    return await zip_codes.all().limit(limit).offset(skip)


@router.post('/favourite_zip_code/{zip_code}', status_code=status.HTTP_200_OK, response_model=FavouriteZipCodeResult)
async def add_favourite_zip_code(
    zip_code: str,
    current_user: User = Depends(get_current_user),
):
    zip_code_object, _ = await ZipCode.get_or_create(code=zip_code)
    await current_user.favourites.add(zip_code_object)

    return zip_code_object


@router.delete('/favourite_zip_code/{zip_code}', response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def remove_favourite_zip_code(
    zip_code: str,
    current_user: User = Depends(get_current_user),
):
    zip_code_to_remove = await ZipCode.get(code=zip_code)
    if not zip_code_to_remove:
        raise HTTPException(status_code=404, detail=f'Zip Code {zip_code} not found.')

    await current_user.favourites.remove(zip_code_to_remove)

    return Status(message=f'Removed Zip Code {zip_code} from favourites')
