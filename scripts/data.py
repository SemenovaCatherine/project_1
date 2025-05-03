import requests
import pandas as pd
from datetime import datetime
from script.config import API_KEY

def fetch_weather_data(city):
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    records = []
    for entry in data['list']:
        record = {
            'datetime': datetime.fromtimestamp(entry['dt']),
            'temperature': entry['main']['temp'],
            'rain': entry.get('rain', {}).get('3h', 0.0),
            'city': city
        }
        records.append(record)
    
    return pd.DataFrame(records)
    
if response.status_code != 200:
    raise Exception(f"Ошибка при запросе к API: {response.status_code}")
