import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import City
from .forms import CityForm
import json
from datetime import datetime, timedelta

def autocomplete_city(request):
    query = request.GET.get('term', '')  # Получаем ввод пользователя
    cities = City.objects.filter(name__icontains=query)[:8]  # Ищем похожие города, возвращаем первые 8
    results = [city.name for city in cities]
    return JsonResponse(results, safe=False)

def index(request):
    appid = 'da4b0f65e3152e9f14707a62675d7717'
    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    cities = City.objects.all()
    city = cities[len(cities)-1]
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={appid}"
    response = requests.get(weather_url)
    print(response.text)

    data = response.json()  # Прямо десериализуем JSON
    days_forecast = []
    current_time = datetime.now()
    date_name = "Сегодня"
    for i in range(3):
        forecast_time = current_time + timedelta(days=i)
        forecast_time = forecast_time.replace(hour=12, minute=0, second=0, microsecond=0)
        for forecast in data['list']:
            forecast_dt = datetime.strptime(forecast['dt_txt'], "%Y-%m-%d %H:%M:%S")
            if forecast_dt == forecast_time:
                if i == 1:
                    date_name = "Завтра"
                elif i == 2:
                    date_name = "Послезавтра"
                temp_k = forecast['main']['temp']
                temp_c = temp_k - 273.15
                icon = forecast['weather'][0]['icon']
                days_forecast.append({
                    'city': city,
                    'date': forecast_dt.strftime("%Y-%m-%d"),
                    'date_name': date_name,
                    'temperature': round(temp_c, 2),
                    'icon': icon
                })
                break
    for day in days_forecast:
        print(f"Date: {day['date']}, Temperature: {day['temperature']} K, Icon: {day['icon']}")  
    
    context = {'all_info': days_forecast, 'form': form}
    return render(request, 'weather/index.html', context)