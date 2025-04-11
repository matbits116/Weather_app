from django.shortcuts import render
import requests
import os
from django.conf import settings

def weather(request):
    data = {}
    
    if request.method == 'POST':
        city = request.POST.get('CITY')
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')  # Get from settings.py
        
        if not api_key:
            return render(request, 'weather.html', {
                'error': 'API key not configured'
            })
        
        try:
            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            weather_data = response.json()
            
            # Process data
            data = {
                'city': city,
                'country_code': weather_data['sys']['country'],
                'coordinates': f"{weather_data['coord']['lon']}, {weather_data['coord']['lat']}",
                'temperature': weather_data['main']['temp'],  # Already in Celsius
                'pressure': weather_data['main']['pressure'],
                'humidity': weather_data['main']['humidity'],
                'description': weather_data['weather'][0]['description'].capitalize(),
                'icon': weather_data['weather'][0]['icon'],
            }
            
        except requests.exceptions.RequestException as e:
            data['error'] = f"Error fetching weather data: {str(e)}"
        except (KeyError, ValueError) as e:
            data['error'] = "Invalid weather data received"
    
    return render(request, 'index.html', data)