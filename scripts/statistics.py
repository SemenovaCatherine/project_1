import pandas as pd

def compute_statistics(df):
    if df.empty:
        raise ValueError("DataFrame пуст. Проверьте загруженные данные.")

    stats = df.groupby('city').agg({
        'temperature': ['mean', 'min', 'max'],
        'rain': 'sum'
    })
    stats.columns = ['avg_temp', 'min_temp', 'max_temp', 'total_rain']
    return stats.reset_index()
