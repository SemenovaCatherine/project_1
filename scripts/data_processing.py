import pandas as pd
from config import Config

def process_data():
    df = pd.read_csv(Config.DATA_RAW_PATH)
    
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df['precipitation'] = df['rain'] + df['snow']
    
    daily_stats = df.groupby(['city', 'date']).agg({
        'temp': ['mean', 'min', 'max'],
        'precipitation': 'sum',
        'humidity': 'mean',
        'wind_speed': 'mean'
    }).reset_index()
    
    daily_stats.columns = ['_'.join(col).strip('_') for col in daily_stats.columns]
    daily_stats.rename(columns={
        'city_': 'city',
        'date_': 'date',
        'temp_mean': 'avg_temp',
        'temp_min': 'min_temp',
        'temp_max': 'max_temp',
        'precipitation_sum': 'total_precipitation',
        'humidity_mean': 'avg_humidity',
        'wind_speed_mean': 'avg_wind_speed'
    }, inplace=True)
    
    daily_stats.to_csv(Config.DATA_PROCESSED_PATH, index=False)
    return daily_stats

if __name__ == "__main__":
    stats = process_data()
    print(f"Обработанные данные сохранены в {Config.DATA_PROCESSED_PATH}")
