from pydantic import BaseModel


class WeatherResult(BaseModel):
    zip_code: str
    detailed_status: str
    temperature: float
    wind_speed: float
    pressure: int
    humidity: int
    location_name: str


class FavouriteZipCodeResult(BaseModel):
    code: str
