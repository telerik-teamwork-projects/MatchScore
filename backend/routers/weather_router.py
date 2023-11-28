import os

import geocoder
from dotenv import load_dotenv
from fastapi import APIRouter, Request
import requests

from common.exceptions import NotFound, Unauthorized, InternalServerError
from models.weather import Geolocation, Weather

router = APIRouter()
load_dotenv()

API_KEY = os.environ['WEATHER_KEY']
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


@router.post('/', response_model=Weather)
def get_weather(request: Request, location: Geolocation | None = None):
    if location is not None:
        if location.city is not None:
            filters = f'q={location.city}'
        else:
            filters = f'lat={location.lat:.4f}&lon={location.lon:.4f}'
    else:
        client = request.client.host
        g = geocoder.ip(client)
        if g.latlng:
            lat, lon = g.latlng
        else:
            g = geocoder.ip('me')
            lat, lon = g.latlng
        filters = f'lat={lat:.4f}&lon={lon:.4f}'
    url = f'http://api.openweathermap.org/data/2.5/weather?{filters}&units=metric&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_id = data["weather"][0]["id"]
        weather_symbol, = _select_weather_display_params(weather_id)
        return Weather.from_query_result(f"{data['name']}", f"{weather_symbol}",
                                         f"{data['weather'][0]['description'].capitalize()}",
                                         f"{data['main']['temp']:.1f}°C", f"{data['main']['feels_like']:.1f}°C",
                                         f"Temperature from {data['main']['temp_min']:.1f} to {data['main']['temp_max']:.1f}°С",
                                         f"{data['wind']['speed']} m/s",
                                         f"{data['main']['humidity']}")

    else:
        if response.status_code == 404:
            raise NotFound(f"Can't find weather data.")
        elif response.status_code == 401:
            raise Unauthorized("Access denied. Check your API key.")
        else:
            raise InternalServerError(f"Something went wrong... ({response.status_code} {response.text})")


def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥",)
    elif weather_id in DRIZZLE:
        display_params = ("💧",)
    elif weather_id in RAIN:
        display_params = ("💦",)
    elif weather_id in SNOW:
        display_params = ("⛄️",)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀",)
    elif weather_id in CLEAR:
        display_params = ("🔆",)
    elif weather_id in CLOUDY:
        display_params = ("💨",)
    else:  # In case the API adds new weather codes
        display_params = ("🌈",)

    return display_params
