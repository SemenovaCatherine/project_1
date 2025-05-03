import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_temperature(df):
    sns.set(style="darkgrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='datetime', y='temperature', hue='city')
    plt.title('Температура по городам')
    plt.xticks(rotation=45)
    os.makedirs('dashboard/figures', exist_ok=True)
    plt.savefig('dashboard/figures/temperature.png')
    plt.close()

def plot_rain(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='city', y='rain', estimator=sum, ci=None)
    plt.title('Суммарные осадки по городам')
    os.makedirs('dashboard/figures', exist_ok=True)
    plt.savefig('dashboard/figures/rain.png')
    plt.close()