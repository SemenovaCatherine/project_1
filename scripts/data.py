import requests
import pandas as pd
from datetime import datetime
from config import API_KEY
from google.colab import files 

API_KEY = "e19341656f7539e9ac6553c950159dc4" 
CITIES = {
    "Санкт-Петербург": {"lat": 59.93, "lon": 30.31},
    "Москва": {"lat": 55.75, "lon": 37.62},
    "Самара": {"lat": 53.20, "lon": 50.15}
}

for city, coords in CITIES.items():
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric&lang=ru"
    )
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка при получении данных для {city}: {response.status_code}")
        continue
    
    data = response.json()

    df = pd.DataFrame([{
        "datetime": pd.to_datetime(entry["dt"], unit="s"),
        "temp_c": entry["main"]["temp"],
        "feels_like_c": entry["main"]["feels_like"],
        "humidity": entry["main"]["humidity"],
        "pressure": entry["main"]["pressure"],
        "wind_speed_kmh": round(entry["wind"]["speed"] * 3.6, 1),
        "weather": entry["weather"][0]["description"],
        "rain_mm": entry.get("rain", {}).get("3h", 0)
    } for entry in data.get("list", [])])

    filename = f"weather_{city}_realtime.csv"
    df.to_csv(filename, index=False)
    print(f"Файл для {city} сохранён!")

    files.download(filename)  # Автоскачивание
