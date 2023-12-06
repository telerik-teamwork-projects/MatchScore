import os
import unittest
from unittest.mock import Mock, patch

from common.exceptions import NotFound, Unauthorized, InternalServerError

with patch.dict(os.environ, {'WEATHER_KEY': 'TestKey'}):
    from routers import weather_router


class WeatherRouter_Should(unittest.TestCase):

    @patch("routers.weather_router.requests")
    def test_getWeather_returns_Weather_when_locationCity(self, mock_requests):
        mock_symbol = Mock(spec='routers.weather_router._select_weather_display_params')
        mock_symbol.return_value = ("💨",)
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {'weather': [{'id': 804, 'description': 'overcast clouds'}],
                                           'main': {'temp': 25.44, 'feels_like': 26.26, 'temp_min': 22.57,
                                                    'temp_max': 27.01, 'humidity': 85},
                                           'wind': {'speed': 1.54},
                                           'name': 'Florianópolis'}
        mock_requests.get = lambda x: mock_response
        result = weather_router.get_weather(Mock(), Mock(city='TestCity'))
        expected = weather_router.Weather(city='Florianópolis', symbol="💨", description='Overcast clouds',
                                          temperature='25.4°C', feels_like='26.3°C', wind='1.54 m/s',
                                          temp_from='Temperature from 22.6 to 27.0°С', humidity='85')
        self.assertEqual(result, expected)

    @patch("routers.weather_router.requests")
    def test_getWeather_returns_Weather_when_locationLatLon(self, mock_requests):
        mock_symbol = Mock(spec='routers.weather_router._select_weather_display_params')
        mock_symbol.return_value = ("💨",)
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {'weather': [{'id': 804, 'description': 'overcast clouds'}],
                                           'main': {'temp': 25.44, 'feels_like': 26.26, 'temp_min': 22.57,
                                                    'temp_max': 27.01, 'humidity': 85},
                                           'wind': {'speed': 1.54},
                                           'name': 'Florianópolis'}
        mock_requests.get = lambda x: mock_response
        result = weather_router.get_weather(Mock(), Mock(lat=-48.5012, lon=-27.6146, city=None))
        expected = weather_router.Weather(city='Florianópolis', symbol="💨", description='Overcast clouds',
                                          temperature='25.4°C', feels_like='26.3°C', wind='1.54 m/s',
                                          temp_from='Temperature from 22.6 to 27.0°С', humidity='85')
        self.assertEqual(result, expected)

    @patch("routers.weather_router.geocoder")
    @patch("routers.weather_router.requests")
    def test_getWeather_returns_Weather_when_locationNoneRequestIp(self, mock_requests, mock_geocoder):
        mock_symbol = Mock(spec='routers.weather_router._select_weather_display_params')
        mock_symbol.return_value = ("💨",)
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {'weather': [{'id': 804, 'description': 'overcast clouds'}],
                                           'main': {'temp': 25.44, 'feels_like': 26.26, 'temp_min': 22.57,
                                                    'temp_max': 27.01, 'humidity': 85},
                                           'wind': {'speed': 1.54},
                                           'name': 'Florianópolis'}
        mock_requests.get = lambda x: mock_response
        mock_request = Mock()
        mock_request.client.host = Mock()
        mock_geocoder.ip = lambda x: Mock(latlng=(-48.5012, -27.6146))
        result = weather_router.get_weather(Mock(), None)
        expected = weather_router.Weather(city='Florianópolis', symbol="💨", description='Overcast clouds',
                                          temperature='25.4°C', feels_like='26.3°C', wind='1.54 m/s',
                                          temp_from='Temperature from 22.6 to 27.0°С', humidity='85')
        self.assertEqual(result, expected)

    @patch("routers.weather_router.geocoder")
    @patch("routers.weather_router.requests")
    def test_getWeather_returns_Weather_when_locationNoneRequestNone(self, mock_requests, mock_geocoder):
        mock_symbol = Mock(spec='routers.weather_router._select_weather_display_params')
        mock_symbol.return_value = ("💨",)
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {'weather': [{'id': 804, 'description': 'overcast clouds'}],
                                           'main': {'temp': 25.44, 'feels_like': 26.26, 'temp_min': 22.57,
                                                    'temp_max': 27.01, 'humidity': 85},
                                           'wind': {'speed': 1.54},
                                           'name': 'Florianópolis'}
        mock_requests.get = lambda x: mock_response
        mock_request = Mock()
        mock_request.client.host = Mock()
        mock_geocoder.ip.side_effect = [Mock(latlng=None), Mock(latlng=(-48.5012, -27.6146))]
        result = weather_router.get_weather(Mock(), None)
        expected = weather_router.Weather(city='Florianópolis', symbol="💨", description='Overcast clouds',
                                          temperature='25.4°C', feels_like='26.3°C', wind='1.54 m/s',
                                          temp_from='Temperature from 22.6 to 27.0°С', humidity='85')
        self.assertEqual(result, expected)

    @patch("routers.weather_router.requests")
    def test_getWeather_raise_NotFound_when_noCity(self, mock_requests):
        mock_requests.get = lambda x: Mock(status_code=404)
        with self.assertRaises(NotFound) as context:
            weather_router.get_weather(Mock(), Mock(city='TestCity'))
        self.assertEqual("Can't find weather data.", context.exception.detail)
        self.assertEqual(404, context.exception.status_code)

    @patch("routers.weather_router.requests")
    def test_getWeather_raise_Unauthorized_when_noKey(self, mock_requests):
        mock_requests.get = lambda x: Mock(status_code=401)
        with self.assertRaises(Unauthorized) as context:
            weather_router.get_weather(Mock(), Mock(city='TestCity'))
        self.assertEqual("Access denied. Check your API key.", context.exception.detail)
        self.assertEqual(401, context.exception.status_code)

    @patch("routers.weather_router.requests")
    def test_getWeather_raise_InternalServerError_when_unexpectedError(self, mock_requests):
        mock_requests.get = lambda x: Mock(status_code=500, text="Some error")
        with self.assertRaises(InternalServerError) as context:
            weather_router.get_weather(Mock(), Mock(city='TestCity'))
        self.assertEqual("Something went wrong... (500 Some error)", context.exception.detail)
        self.assertEqual(500, context.exception.status_code)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_THUNDERSTORM(self):
        result = weather_router._select_weather_display_params(201)
        expected = ("💥",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_DRIZZLE(self):
        result = weather_router._select_weather_display_params(301)
        expected = ("💧",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_RAIN(self):
        result = weather_router._select_weather_display_params(501)
        expected = ("💦",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_SNOW(self):
        result = weather_router._select_weather_display_params(601)
        expected = ("⛄️",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_ATMOSPHERE(self):
        result = weather_router._select_weather_display_params(701)
        expected = ("🌀",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_CLEAR(self):
        result = weather_router._select_weather_display_params(800)
        expected = ("🔆",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_CLOUDY(self):
        result = weather_router._select_weather_display_params(801)
        expected = ("💨",)
        self.assertEqual(result, expected)

    def test__selectWeatherDisplayParams_returns_correctIcon_when_newApiCode(self):
        result = weather_router._select_weather_display_params(1001)
        expected = ("🌈",)
        self.assertEqual(result, expected)
