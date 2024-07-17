"""main application module"""

import uvicorn
from fastapi import FastAPI
from routes.weather_route import weather_route


DESCRIPTION = 'Application based on FastApi framework to get weather forecast. On main page visitor write name of needed city and choose weekly or hourly forecast. Weather data gets from open-meteo api. '

app = FastAPI(
    title='Weather app',
    description=DESCRIPTION,
    version='0.0.1',
    contact={
        'email': 'Popov.a.al@parallax.ru'
    }
)


MEDIA_TYPE = 'multipart/x-mixed-replace;boundary=frame'

app.include_router(weather_route)

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)
