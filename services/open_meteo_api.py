"""service module to get forecast data"""
from open_meteo import OpenMeteo
from open_meteo.exceptions import OpenMeteoConnectionError
from open_meteo.models import DailyParameters, HourlyParameters


async def get_forecast(city:str, dates:str)-> dict or None:
    """func to get weather forecast from city name"""
    if city is None:
        return None
    try:
        forecast_data = await OpenMeteo().geocoding(name=city)  # get city geocoding parameters
        if forecast_data.results is None:  # if city not finded, return None
            return None
        else:
            city_latitude = forecast_data.to_dict()['results'][0]['latitude']  # latitude of needed city
            city_longitude = forecast_data.to_dict()['results'][0]['longitude']  # longitude of needed city
            async with OpenMeteo() as open_meteo:
                if dates=='week':  # get week forecast
                    forecast = await open_meteo.forecast(
                                                latitude=city_latitude,
                                                longitude=city_longitude,
                                                current_weather=True,
                                            daily=[
                                                DailyParameters.TEMPERATURE_2M_MAX,
                                                DailyParameters.PRECIPITATION_SUM,
                                                DailyParameters.WIND_SPEED_10M_MAX,
                                                    ]
                                                )
                    temperatures = forecast.daily.to_dict()['temperature_2m_max']
                    precipitation = forecast.daily.to_dict()['precipitation_sum']
                    wind = forecast.daily.to_dict()['wind_speed_10m_max']
                    time = forecast.daily.to_dict()['time']

                    return {"temperatures":temperatures, "precipitation":precipitation, "time":time, 'wind':wind, 'week':True}

                elif dates=='hour':  # hourly forecast for today date
                    forecast = await open_meteo.forecast(
                                                latitude=city_latitude,
                                                longitude=city_longitude,
                                                current_weather=True,
                                            hourly=[
                                                HourlyParameters.APPARENT_TEMPERATURE,
                                                    ],
                                                )
                    hours = forecast.hourly.time[7:22]
                    temperatures = forecast.hourly.apparent_temperature[7:22]
                    return {'time':hours, 'temperatures':temperatures, 'wind':None, 'precipitation': None, 'week':False}
    except OpenMeteoConnectionError:  # No connection with https:/open-meteo.com
        return None
