"""Base route to get weather forecast"""
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from services.open_meteo_api import get_forecast


templates = Jinja2Templates(directory='templates')

weather_route = APIRouter()

@weather_route.get('/')
async def greeting_route(request: Request):
    """Returns main page"""
    return templates.TemplateResponse({'request':request}, 'base.html')


@weather_route.post('/')
async def show_weather(request: Request,
                        city: str= Form(None),
                       dates: str = Form(None)):
    """Get values from form, and returns to user weather forecast"""
    weather = await get_forecast(city=city, dates=dates)
    if weather is None:
        return templates.TemplateResponse('base.html', {'request':request,"msg":"Проверьте подключение к интернету или правильность написания города. Подсказка: попробуйте написать город на английском языке"})
    else:
        return templates.TemplateResponse('base.html', {'request':request,
                                                    'temperatures':weather['temperatures'],
                                                    'time':weather['time'],
                                                    'wind':weather['wind'],
                                                    'precipitation':weather['precipitation'],
                                                    'week':weather['week']})
