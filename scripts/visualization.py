import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from datetime import datetime

# Создаем папку для графиков
os.makedirs('dashboard/figures', exist_ok=True)

def load_and_prepare_data():
    # Загрузка данных
    cities = ['Москва', 'Санкт-Петербург', 'Самара']
    dfs = []
    
    for city in cities:
        filename = f'weather_{city}_realtime.csv'
        df = pd.read_csv(filename)
        df['city'] = city
        df['datetime'] = pd.to_datetime(df['datetime'])
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

def plot_temperature(df):
    plt.figure(figsize=(14, 7))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    
    # График температуры
    ax = sns.lineplot(data=df, x='datetime', y='temp_c', hue='city', 
                      palette=['#1f77b4', '#ff7f0e', '#2ca02c'], linewidth=2)
    
    plt.title('Изменение температуры по городам (5 дней)', fontsize=14, pad=20)
    plt.xlabel('Дата и время', fontsize=12)
    plt.ylabel('Температура (°C)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Улучшаем легенду
    plt.legend(title='Город', title_fontsize=12, fontsize=11)
    
    # Сохраняем график
    plt.tight_layout()
    plt.savefig('dashboard/figures/temperature.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_rain(df):
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Группируем данные по городам и суммируем осадки
    rain_data = df.groupby('city')['rain_mm'].sum().reset_index()
    
    # График осадков
    ax = sns.barplot(data=rain_data, x='city', y='rain_mm', 
                     palette=['#1f77b4', '#ff7f0e', '#2ca02c'], edgecolor='black')
    
    plt.title('Суммарные осадки по городам (5 дней)', fontsize=14, pad=20)
    plt.xlabel('Город', fontsize=12)
    plt.ylabel('Осадки (мм)', fontsize=12)
    
    # Добавляем значения на столбцы
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f} мм", 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='center', xytext=(0, 10), 
                   textcoords='offset points', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('dashboard/figures/rain.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_humidity_pressure(df):
    plt.figure(figsize=(14, 7))
    sns.set_style("darkgrid")
    
    # Два подграфика
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Влажность
    sns.lineplot(data=df, x='datetime', y='humidity', hue='city', 
                 palette=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax1)
    ax1.set_title('Влажность по городам', fontsize=13)
    ax1.set_xlabel('')
    ax1.set_ylabel('Влажность (%)', fontsize=11)
    ax1.legend(title='Город')
    
    # Давление
    sns.lineplot(data=df, x='datetime', y='pressure', hue='city', 
                 palette=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax2)
    ax2.set_title('Атмосферное давление по городам', fontsize=13)
    ax2.set_xlabel('Дата и время', fontsize=11)
    ax2.set_ylabel('Давление (гПа)', fontsize=11)
    ax2.legend(title='Город')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('dashboard/figures/humidity_pressure.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_weather_stats(df):
    # Создаем сводную статистику
    stats = df.groupby('city').agg({
        'temp_c': ['mean', 'max', 'min'],
        'rain_mm': 'sum',
        'wind_speed_kmh': 'mean'
    }).reset_index()
    
    stats.columns = ['Город', 'Средняя темп.', 'Макс. темп.', 'Мин. темп.', 
                    'Сумма осадков', 'Ср. скорость ветра']
    
    # Создаем таблицу
    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
    table = plt.table(cellText=stats.values,
                     colLabels=stats.columns,
                     loc='center',
                     cellLoc='center',
                     colColours=['#f7f7f7']*len(stats.columns))
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    plt.title('Сводная статистика по погоде (5 дней)', fontsize=14, pad=20)
    plt.savefig('dashboard/figures/weather_stats.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Загрузка и подготовка данных
    df = load_and_prepare_data()
    
    # Создание графиков
    plot_temperature(df)
    plot_rain(df)
    plot_humidity_pressure(df)
    plot_weather_stats(df)
    
    print("Графики успешно сохранены в папку dashboard/figures/")

if __name__ == "__main__":
    main()
