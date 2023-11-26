from pydantic import BaseModel


class Geolocation(BaseModel):
    lat: float | None = None
    lon: float | None = None
    city: str | None = None


class Weather(BaseModel):
    city: str
    symbol: str
    description: str
    temperature: str
    feels_like: str
    temp_from: str
    wind: str
    humidity: str

    @classmethod
    def from_query_result(cls, city, symbol, description, temp, feels_like, temp_from, wind, humidity):
        return cls(
            city=city,
            symbol=symbol,
            description=description,
            temperature=temp,
            feels_like=feels_like,
            temp_from=temp_from,
            wind=wind,
            humidity=humidity
        )
