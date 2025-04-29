import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("Анализ отзывов с Ozon")

df = pd.read_csv("data/ozon_reviews.csv")

st.write("Всего отзывов:", len(df))

category = st.selectbox("Выберите категорию:", df['category'].unique())

df_cat = df[df['category'] == category]

st.subheader(f"Средняя оценка ({category}): {df_cat['rating'].mean():.2f}")
st.subheader(f"Средняя длина отзыва: {df_cat['text'].apply(lambda x: len(str(x).split())).mean():.1f} слов")

text = " ".join(df_cat['text'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)
