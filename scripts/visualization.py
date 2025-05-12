import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
import os

# Создаем папку для сохранения графиков
os.makedirs('dashboard/figures', exist_ok=True)

def plot_temperature_trend(df):
    """1. Линейный график температуры (Seaborn)"""
    plt.figure(figsize=(14, 7))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    
    ax = sns.lineplot(
        data=df, 
        x='datetime', 
        y='temp_c', 
        hue='city',
        palette=['#1f77b4', '#ff7f0e', '#2ca02c'],
        linewidth=2,
        style='city',
        markers=True
    )
    
    plt.title('Динамика температуры по городам', fontsize=16, pad=20)
    plt.xlabel('Дата и время', fontsize=12)
    plt.ylabel('Температура (°C)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Город', title_fontsize=12, fontsize=11, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('dashboard/figures/temperature_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_weather_wordcloud(df):
    """2. Облако тегов погодных условий (WordCloud)"""
    from collections import Counter
    
    # Собираем все описания погоды
    weather_text = ' '.join(df['weather'].dropna())
    word_counts = Counter(weather_text.split())
    
    # Создаем облако слов
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=50
    ).generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Частота погодных условий', fontsize=16, pad=20)
    plt.axis('off')
    
    plt.savefig('dashboard/figures/weather_wordcloud.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_interactive_temp_map(df):
    """3. Интерактивная карта температур (Plotly)"""
    # Создаем усредненные данные по городам
    avg_temp = df.groupby('city', as_index=False)['temp_c'].mean()
    
    # Координаты городов (широта, долгота)
    city_coords = {
        'Москва': [55.7558, 37.6173],
        'Санкт-Петербург': [59.9343, 30.3351],
        'Самара': [53.1951, 50.1009]
    }
    
    avg_temp['lat'] = avg_temp['city'].map(lambda x: city_coords[x][0])
    avg_temp['lon'] = avg_temp['city'].map(lambda x: city_coords[x][1])
    
    fig = px.scatter_mapbox(
        avg_temp,
        lat='lat',
        lon='lon',
        size='temp_c',
        color='temp_c',
        hover_name='city',
        hover_data={'temp_c': ':.1f'},
        size_max=30,
        zoom=3,
        color_continuous_scale=px.colors.sequential.Tealrose,
        title='Средняя температура по городам'
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        title_x=0.5,
        title_font_size=20
    )
    
    fig.write_html('dashboard/figures/interactive_temp_map.html')

def generate_visualizations(df):
    """Генерация всех визуализаций"""
    plot_temperature_trend(df)
    plot_weather_wordcloud(df)
    plot_interactive_temp_map(df)
    print("Визуализации успешно сохранены в папку dashboard/figures/")
