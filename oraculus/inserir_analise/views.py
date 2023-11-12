from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from resultado.views import resultado
from analise.models import Analise, ConfiguracaoAlgoritmo
from django.utils import timezone
from datetime import date
from django.http import JsonResponse
from django.contrib import messages

import numpy as np
import pandas as pd
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
import seaborn as sns
import matplotlib.pyplot as plt

# Preparar as escalas ph e rainfall
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

from django.contrib.auth.models import User


@login_required
def inserir_analise(request):
    modelos = ConfiguracaoAlgoritmo.objects.all()
    return render(request, "inserir_analise.html", {'modelos': modelos})

def configura_algoritmo(request):
    return render(request, "configura_algoritmo.html")

def treinar_algoritmo(request):

    qtdTeste = request.POST.get('qtdTeste')
    qtdVizinhos = request.POST.get('qtdVizinhos')
    algoritmo = request.POST.get('algoritmo')
    pesos = request.POST.get('pesos')

    qtdTeste = float(qtdTeste)
    qtdTeste = qtdTeste / 100
    qtdVizinhos = int(qtdVizinhos)

    # Leitura do csv
    df=pd.read_csv('crop.csv')

    # Preparo da IA para entender os dados
    c=df.label.astype('category')
    targets = dict(enumerate(c.cat.categories))
    df['target']=c.cat.codes

    y=df.target
    X=df[['N','P','K','temperature','humidity','ph','rainfall']]

    X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1, test_size=qtdTeste)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=qtdVizinhos, algorithm=algoritmo, weights=pesos)
    knn.fit(X_train_scaled, y_train)

    acuracia_modelo = knn.score(X_test_scaled, y_test)
    acuracia = round((acuracia_modelo * 100), 3)

    dados_algoritmo= {
        'knn': knn,
        'X_train': X_train,
        'targets': targets,
        'qtdTeste': qtdTeste,
        'qtdVizinhos': qtdVizinhos,
        'algoritmo': algoritmo,
        'pesos': pesos,
        'acuracia': acuracia
    }

    return render(request, 'configura_algoritmo.html', dados_algoritmo)

def salvar_algoritmo(request):
    
    qtdTeste = request.POST.get('qtdTeste')
    qtdVizinhos = request.POST.get('qtdVizinhos')
    algoritmo = request.POST.get('algoritmo')
    pesos = request.POST.get('pesos')
    acuracia = request.POST.get('acuracia')

    qtdTeste = float(qtdTeste.replace(',', '.'))
    acuracia = float(acuracia.replace(',', '.'))

    usuario = User.objects.get(username='m4ec')

    infos_algoritmo = ConfiguracaoAlgoritmo(
        usuario=usuario,
        qtdTeste=qtdTeste,
        qtdVizinhos=qtdVizinhos,
        algoritmo=algoritmo,
        pesos=pesos,
        acuracia=acuracia,
    )
    
    infos_algoritmo.save()

    messages.success(request, "Modelo salvo com sucesso")

    return redirect(configura_algoritmo)

def selecionar_modelo(request):
    modelos = ConfiguracaoAlgoritmo.objects.all() 

    if request.method == 'POST':
        modelo_id = request.POST.get('label')


        if modelo_id == 'Padrão':
            acuracia = 97.636
            qtdTeste = 0.25
            qtdVizinhos = 5
            algoritmo = 'auto'
            pesos = 'uniform'
        else:
            modelo = ConfiguracaoAlgoritmo.objects.get(id=modelo_id)
            acuracia = modelo.acuracia
            qtdTeste = modelo.qtdTeste
            qtdVizinhos = modelo.qtdVizinhos
            algoritmo = modelo.algoritmo
            pesos = modelo.pesos

        return render(request, 'inserir_analise.html', {
            'modelos': modelos,
            'id': modelo_id,
            'acuracia': acuracia,
            'qtdTeste': qtdTeste,
            'qtdVizinhos': qtdVizinhos,
            'algoritmo': algoritmo,
            'pesos': pesos,
        })

def fazer_previsao_knn(modelo, dados_de_entrada):
    # Leitura do csv
    df=pd.read_csv('crop.csv')

    # Preparo da IA para entender os dados
    c=df.label.astype('category')
    targets = dict(enumerate(c.cat.categories))
    df['target']=c.cat.codes

    y=df.target
    X=df[['N','P','K','temperature','humidity','ph','rainfall']]

    X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1, test_size=0.25)
    
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    dados_de_entrada_padronizados = scaler.transform(dados_de_entrada.reshape(1, -1))

    # Faça a previsão com o modelo
    previsao = modelo.predict(dados_de_entrada_padronizados)
    colheita_prevista = targets.get(previsao[0])

    return colheita_prevista

def rodar_algoritmo_analise(request):

    id_modelo = request.POST.get('id_modelo')
    qtdTeste = request.POST.get('qtdTeste')
    qtdVizinhos = request.POST.get('qtdVizinhos')
    algoritmo = request.POST.get('algoritmo')
    pesos = request.POST.get('pesos')
    acuracia = request.POST.get('acuracia')

    qtdTeste = float(qtdTeste.replace(',', '.'))
    qtdVizinhos = int(qtdVizinhos)
    acuracia = float(acuracia.replace(',', '.'))

    N = request.POST.get('N')
    P = request.POST.get('P')
    K = request.POST.get('K')
    Temperatura = request.POST.get('Temperatura')
    Umidade = request.POST.get('Umidade')
    pH = request.POST.get('pH')
    Chuva = request.POST.get('Chuva')

    dados_analise = np.array([N, P, K, Temperatura, Umidade, pH, Chuva])

    df=pd.read_csv('crop.csv')

    c=df.label.astype('category')
    targets = dict(enumerate(c.cat.categories))
    df['target']=c.cat.codes

    y=df.target
    X=df[['N','P','K','temperature','humidity','ph','rainfall']]

    X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1, test_size=qtdTeste)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=qtdVizinhos, algorithm=algoritmo, weights=pesos)
    knn.fit(X_train_scaled, y_train)
    knn.score(X_test_scaled, y_test)

    colheita_prevista = fazer_previsao_knn(knn, dados_analise)

    dados_filtrados = df[df['label'] == colheita_prevista]

    # Calculando a média
    media_n = dados_filtrados['N'].mean()
    media_p = dados_filtrados['P'].mean()
    media_k = dados_filtrados['K'].mean()
    media_temperature = dados_filtrados['temperature'].mean()
    media_humidity = dados_filtrados['humidity'].mean()
    media_ph = dados_filtrados['ph'].mean()
    media_rainfall = dados_filtrados['rainfall'].mean()

    #Calculando o desvio padrão
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
        'id_modelo': id_modelo,
        'acuracia' : acuracia,
        'qtdTeste' : qtdTeste,
        'qtdVizinhos' : qtdVizinhos,
        'algoritmo' : algoritmo,
        'pesos' : pesos,
        'colheita_prevista': colheita_prevista,
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
    }

    return render(request, 'resultado.html', context)




