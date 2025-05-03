import requests
import pandas as pd
from datetime import datetime
from config import Config

def get_weather_data(city):
    params = {
        'q': city,
        'appid': Config.API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(Config.BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def process_weather_data(data):
    processed_data = []
    for entry in data['list']:
        processed_data.append({
            'city': data['city']['name'],
            'date': datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d'),
            'time': datetime.fromtimestamp(entry['dt']).strftime('%H:%M'),
            'temp': entry['main']['temp'],
            'feels_like': entry['main']['feels_like'],
            'humidity': entry['main']['humidity'],
            'pressure': entry['main']['pressure'],
            'weather': entry['weather'][0]['description'],
            'wind_speed': entry['wind']['speed'],
            'clouds': entry['clouds']['all'],
            'rain': entry.get('rain', {}).get('3h', 0),
            'snow': entry.get('snow', {}).get('3h', 0)
        })
    return pd.DataFrame(processed_data)

def save_weather_data():
    all_data = pd.DataFrame()
    for city in Config.CITIES:
        print(f"Получаем данные для {city}...")
        data = get_weather_data(city)
        city_df = process_weather_data(data)
        all_data = pd.concat([all_data, city_df])
    
    all_data.to_csv(Config.DATA_RAW_PATH, index=False)
    return all_data

if __name__ == "__main__":
    weather_data = save_weather_data()
    print(f"Данные сохранены в {Config.DATA_RAW_PATH}")
