from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
import pandas as pd

df=pd.read_csv('crop.csv')
print(df.describe())

@login_required
def recomendar_colheita(request):
    return render(request, "recomendar_colheita.html")

def carregar_dados_csv():
    df=pd.read_csv('crop.csv')
    return df

def enviar_colheita(request):
    if request.method == 'POST':
        label_selecionado = request.POST['label']

        return label_selecionado
    
def calcular_media(request):
    if request.method == 'POST':
        label_selecionado = request.POST['label']

        # Lê o arquivo CSV
        df = pd.read_csv('crop.csv')

        # Filtra os dados com base no rótulo selecionado
        dados_filtrados = df[df['label'] == label_selecionado]

        # Calculando a média
        media_n = dados_filtrados['N'].mean()
        media_p = dados_filtrados['P'].mean()
        media_k = dados_filtrados['K'].mean()
        media_temperature = dados_filtrados['temperature'].mean()
        media_humidity = dados_filtrados['humidity'].mean()
        media_ph = dados_filtrados['ph'].mean()
        media_rainfall = dados_filtrados['rainfall'].mean()

        # Calculando o mínimo
        min_n = dados_filtrados['N'].min()
        min_p = dados_filtrados['P'].min()
        min_k = dados_filtrados['K'].min()
        min_temperature = dados_filtrados['temperature'].min()
        min_humidity = dados_filtrados['humidity'].min()
        min_ph = dados_filtrados['ph'].min()
        min_rainfall = dados_filtrados['rainfall'].min()

        # Calculando o máximo
        max_n = dados_filtrados['N'].max()
        max_p = dados_filtrados['P'].max()
        max_k = dados_filtrados['K'].max()
        max_temperature = dados_filtrados['temperature'].max()
        max_humidity = dados_filtrados['humidity'].max()
        max_ph = dados_filtrados['ph'].max()
        max_rainfall = dados_filtrados['rainfall'].max()

        # Calculando o desvio padrão
        std_n = dados_filtrados['N'].std()
        std_p = dados_filtrados['P'].std()
        std_k = dados_filtrados['K'].std()
        std_temperature = dados_filtrados['temperature'].std()
        std_humidity = dados_filtrados['humidity'].std()
        std_ph = dados_filtrados['ph'].std()
        std_rainfall = dados_filtrados['rainfall'].std()

        context = {
        'colheita': label_selecionado,
        'media_n': round(media_n, 2),
        'media_p': round(media_p, 2),
        'media_k': round(media_k, 2),
        'media_temperature': round(media_temperature, 2),
        'media_humidity': round(media_humidity, 2),
        'media_ph': round(media_ph, 2),
        'media_rainfall': round(media_rainfall, 2),
        'min_n': round(min_n, 2),
        'min_p': round(min_p, 2),
        'min_k': round(min_k, 2),
        'min_temperature': round(min_temperature, 2),
        'min_humidity': round(min_humidity, 2),
        'min_ph': round(min_ph, 2),
        'min_rainfall': round(min_rainfall, 2),
        'max_n': round(max_n, 2),
        'max_p': round(max_p, 2),
        'max_k': round(max_k, 2),
        'max_temperature': round(max_temperature, 2),
        'max_humidity': round(max_humidity, 2),
        'max_ph': round(max_ph, 2),
        'max_rainfall': round(max_rainfall, 2),
        'std_n': round(std_n, 2),
        'std_p': round(std_p, 2),
        'std_k': round(std_k, 2),
        'std_temperature': round(std_temperature, 2),
        'std_humidity': round(std_humidity, 2),
        'std_ph': round(std_ph, 2),
        'std_rainfall': round(std_rainfall, 2),
}


        return render(request, 'recomendar_colheita.html', context)

   



