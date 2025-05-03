import streamlit as st
import pandas as pd
import plotly.express as px
from config import Config

@st.cache_data
def load_data():
    return pd.read_csv(Config.DATA_PROCESSED_PATH)

def main():
    st.set_page_config(page_title="Weather Dashboard", layout="wide")
    st.title("Сравнение погодных условий")
    
    df = load_data()
    
    st.sidebar.header("Фильтры")
    cities = st.sidebar.multiselect(
        "Города", 
        df['city'].unique(), 
        default=df['city'].unique()
    )
    
    date_range = st.sidebar.select_slider(
        "Диапазон дат",
        options=sorted(df['date'].unique()),
        value=(df['date'].min(), df['date'].max())
    )
    
    filtered_df = df[
        (df['city'].isin(cities)) & 
        (df['date'] >= date_range[0]) & 
        (df['date'] <= date_range[1])
    ]
    
    tab1, tab2, tab3 = st.tabs(["Температура", "Осадки", "Статистика"])
    
    with tab1:
        st.plotly_chart(
            px.line(
                filtered_df, x='date', y='avg_temp', color='city',
                title='Среднесуточная температура'
            ),
            use_container_width=True
        )
    
    with tab2:
        st.plotly_chart(
            px.bar(
                filtered_df, x='date', y='total_precipitation', color='city',
                title='Суммарные осадки'
            ),
            use_container_width=True
        )
    
    with tab3:
        st.dataframe(
            filtered_df.groupby('city').agg({
                'avg_temp': 'mean',
                'total_precipitation': 'sum',
                'avg_humidity': 'mean'
            }).rename(columns={
                'avg_temp': 'Ср. температура',
                'total_precipitation': 'Всего осадков',
                'avg_humidity': 'Ср. влажность'
            }),
            use_container_width=True
        )

if __name__ == "__main__":
    main()
