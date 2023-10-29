from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from resultado.views import resultado
from analise.models import AnaliseSolo, Analise, ConfiguracaoAlgoritmo
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

@login_required
def inserir_analise(request):
    return render(request, "inserir_analise.html")

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

    infos_algoritmo = ConfiguracaoAlgoritmo(
        qtdTeste=qtdTeste,
        qtdVizinhos=qtdVizinhos,
        algoritmo=algoritmo,
        pesos=pesos,
        acuracia=acuracia,
    )
    infos_algoritmo.save()

    messages.success(request, "Modelo salvo com sucesso")

    return redirect(configura_algoritmo)


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

def salvar_algoritmo_analise(request):

    N = request.POST.get('N')
    P = request.POST.get('P')
    K = request.POST.get('K')
    Temperatura = request.POST.get('Temperatura')
    Umidade = request.POST.get('Umidade')
    pH = request.POST.get('pH')
    Chuva = request.POST.get('Chuva')

    dados_analise = np.array([N, P, K, Temperatura, Umidade, pH, Chuva])

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
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=5, algorithm='auto', weights='uniform')
    knn.fit(X_train_scaled, y_train)
    knn.score(X_test_scaled, y_test)

    colheita_prevista = fazer_previsao_knn(knn, dados_analise)

    inclusao_colheita = Analise(
            N=N,
            P=P,
            K=K,
            Temperatura=Temperatura,
            Umidade=Umidade,
            pH=pH,
            Chuva=Chuva,
            Colheita=colheita_prevista,
        )

    inclusao_colheita.save()

    context = {
        'colheita_prevista': colheita_prevista,
        'N': N,
        'P': P,
        'K': K,
        'Temperatura': Temperatura,
        'Umidade': Umidade,
        'pH': pH,
        'Chuva': Chuva,
        #'Acuracia': acuracia
    }

    return render(request, 'resultado.html', context)




