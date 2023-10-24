import datetime

import requests
from django.shortcuts import render
import config

API_KEY = config.appid

#to run server use:
#python manage.py runserver

# Create your views here.
def index(request):
    coordinates_url = "http://api.openweathermap.org/geo/1.0/direct?q={},{}&limit=1&appid={}"
    weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=imperial"


    if request.method == "POST":
        city = request.POST["city"]
        state = request.POST["state"]
        
        weather_data, daily_forecasts = fetch_weather(city, state, coordinates_url, weather_url, forecast_url)

        context = {"weather_data": weather_data, "daily_forecasts": daily_forecasts}
        return render(request, "weather_app/index.html", context)

    else:
        return render(request, "weather_app/index.html")
    
def fetch_weather(city, state, coordinates_url, weather_url, forecast_url):
    coord_response = requests.get(coordinates_url.format(city, state, API_KEY)).json()
    lat, lon = coord_response[0]["lat"], coord_response[0]["lon"]
    weather_response = requests.get(weather_url.format(lat, lon, API_KEY)).json()
    forecast_response = requests.get(forecast_url.format(lat, lon, API_KEY)).json()

    weather_data = {
        "city": city,
        "temp": weather_response["main"]["temp"],
        "description": weather_response["weather"][0]["description"],
        "icon": weather_response["weather"][0]["icon"],
    }

    daily_forecasts = []
    for daily_data in forecast_response["list"][:5]:
        daily_forecasts.append(
            {
                "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A %b %d "),
                "min_temp": round(daily_data["main"]["temp_min"], 2),
                "max_temp": round(daily_data["main"]["temp_max"], 2),
                "description": daily_data["weather"][0]["description"],
                "icon": daily_data["weather"][0]["icon"], 
            }
        )
    return weather_data, daily_forecasts
