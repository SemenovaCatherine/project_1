import requests
import pandas as pd
from datetime import datetime
from script.config import API_KEY

def fetch_weather_data(city):
    try:
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params)
        
        # Проверяем статус ответа перед обработкой данных
        response.raise_for_status()  # Поймает ошибки HTTP, такие как 404, 500

        data = response.json()

        # Проверка на корректность данных
        if 'list' not in data:
            raise ValueError(f"Invalid data structure: 'list' not found for {city}")

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

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки

    except ValueError as e:
        print(f"Data error for {city}: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки в данных
