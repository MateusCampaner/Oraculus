from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise, ConfiguracaoAlgoritmo
import pandas as pd
from django.contrib.auth.models import User
from django.http import JsonResponse

@login_required
def acessar_dados(request):
    return render(request, "acessar_dados.html")

def acessar_dados_analise(request):
    if request.user.is_superuser:
        analises = Analise.objects.all()

    elif request.user.is_authenticated:

        analises = Analise.objects.filter(usuario=request.user)
    else:
        analises = []

    return render(request, "acessar_dados_analise.html", {'analises': analises})

def acessar_dados_modelo(request):
    if request.user.is_superuser:
        modelos = ConfiguracaoAlgoritmo.objects.all()

    elif request.user.is_authenticated:

        modelos = ConfiguracaoAlgoritmo.objects.filter(usuario=request.user)
    else:
        modelos = []  
    
    return render(request, "acessar_dados_modelo.html", {"modelos": modelos})

def get_analises(request):
    analises = Analise.objects.all()
    return render(request, 'acessar_dados.html', {'analises': analises})

def delete_analises(request, id):
    analises = Analise.objects.get(id=id)
    analises.delete()
    return redirect(acessar_dados_analise)

def visualizar_analise(request, id):
    analises = Analise.objects.get(id=id)

    # Lê o arquivo CSV
    df = pd.read_csv('crop.csv')
    # Filtra os dados com base no rótulo selecionado
    dados_filtrados = df[df['label'] == analises.Colheita]

    N = analises.N
    P = analises.P
    K = analises.K
    Temperatura = analises.Temperatura
    Umidade = analises.Umidade
    pH = analises.pH
    Chuva = analises.Chuva
    Colheita = analises.Colheita
    id = analises.id
    data_analise = analises.data_analise
    usuario = analises.usuario
    configuracao_algoritmo = analises.configuracao_algoritmo

    # Calculando a média
    media_n = dados_filtrados['N'].mean()
    media_p = dados_filtrados['P'].mean()
    media_k = dados_filtrados['K'].mean()
    media_temperature = dados_filtrados['temperature'].mean()
    media_humidity = dados_filtrados['humidity'].mean()
    media_ph = dados_filtrados['ph'].mean()
    media_rainfall = dados_filtrados['rainfall'].mean()

    # Calculando o desvio padrão
    std_n = dados_filtrados['N'].std()
    std_p = dados_filtrados['P'].std()
    std_k = dados_filtrados['K'].std()
    std_temperature = dados_filtrados['temperature'].std()
    std_humidity = dados_filtrados['humidity'].std()
    std_ph = dados_filtrados['ph'].std()
    std_rainfall = dados_filtrados['rainfall'].std()

    N = int(N)
    P = int(P)
    K = int(K)
    Temperatura = float(Temperatura)
    Umidade = float(Umidade)
    pH = float(pH)
    Chuva = float(Chuva)

    #Calculando o Score-Z
    scoreZ_n = (N - media_n) / std_n
    scoreZ_p = (P - media_p) / std_p
    scoreZ_k = (K - media_k) / std_k
    scoreZ_temperature = (Temperatura - media_temperature) / std_temperature
    scoreZ_humidity = (Umidade - media_humidity) / std_humidity
    scoreZ_ph = (pH - media_ph) / std_ph
    scoreZ_rainfall = (Chuva - media_rainfall) / std_rainfall


    context = {
        'Colheita': Colheita,
        'id': id,
        'data_analise': data_analise,
        'usuario': usuario,
        'N': N,
        'P': P,
        'K': K,
        'Temperatura': Temperatura,
        'Umidade': Umidade,
        'pH': pH,
        'Chuva': Chuva,
        'scoreZ_n': round(scoreZ_n, 2),
        'scoreZ_p': round(scoreZ_p, 2),
        'scoreZ_k': round(scoreZ_k, 2),
        'scoreZ_temperature': round(scoreZ_temperature, 2),
        'scoreZ_humidity': round(scoreZ_humidity, 2),
        'scoreZ_ph': round(scoreZ_ph, 2),
        'scoreZ_rainfall': round(scoreZ_rainfall, 2),
        'configuracao_algoritmo': configuracao_algoritmo,
    }

    return render(request, 'visualizar_analise.html', context)

def get_modelos(request):
    modelos = ConfiguracaoAlgoritmo.objects.all()
    return render(request, 'acessar_dados.html', {'modelos': modelos})

def delete_modelos(request, id):
    modelos = ConfiguracaoAlgoritmo.objects.get(id=id)
    modelos.delete()
    return redirect(acessar_dados_modelo)

def visualizar_modelo(request, id):
    modelos = ConfiguracaoAlgoritmo.objects.get(id=id)
    return render(request, 'visualizar_modelo.html', {'modelos': modelos})


