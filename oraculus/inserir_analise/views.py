from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from resultado.views import resultado
from inserir_analise.forms import AnaliseSoloForm, AnaliseForm, ConfiguracaoAlgoritmoForm
from analise.models import AnaliseSolo, Analise, ConfiguracaoAlgoritmo
from django.utils import timezone
from datetime import date
from django.http import JsonResponse

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


    infos_algoritmo = ConfiguracaoAlgoritmo(
        qtdTeste=qtdTeste,
        qtdVizinhos=qtdVizinhos,
        algoritmo=algoritmo,
        pesos=pesos,
        acuracia=acuracia,
    )
    infos_algoritmo.save()


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

'''
def rodar_algoritmo_analise(request):
    N = request.POST.get('N')
    P = request.POST.get('P')
    K = request.POST.get('K')
    Umidade = request.POST.get('Umidade')
    Temperatura = request.POST.get('Temperatura')
    pH = request.POST.get('pH')
    Chuva = request.POST.get('Chuva')

    dados_analise = np.array([N, P, K, Umidade, Temperatura, pH, Chuva])

    colheita_prevista = fazer_previsao_knn(knn, dados_analise)

    context = {
        'colheita_prevista': colheita_prevista,
        'N': N,
        'P': P,
        'K': K,
        'Temperatura': Temperatura,
        'Umidade': Umidade,
        'pH': pH,
        'Chuva': Chuva,
    }

    return render(request, 'resultado.html', context)
'''

'''
def rodar_analise(request):
    modelAnaliseSolo = AnaliseSolo
    modelAnalise = Analise
    modelConfiguracaoAlgoritmo = ConfiguracaoAlgoritmo

    formAnaliseSolo = AnaliseSoloForm(request.POST)
    formAnalise = AnaliseForm(request.POST)
    formConfiguracaoAlgoritmo = ConfiguracaoAlgoritmoForm(request.POST)

    if request.method == 'POST':
        # Crie o AnaliseSoloForm com os dados preenchidos automaticamente
        usuario = request.user  # Supondo que você obtém o usuário atual
        analise_solo_form = AnaliseSoloForm(request.POST, user=usuario)

        if analise_solo_form.is_valid():
            # Salve o AnaliseSoloForm
            analise_solo = analise_solo_form.save()

            # Preencha o ConfiguracaoAlgoritmoForm
            configuracao_form = ConfiguracaoAlgoritmoForm(request.POST)
            if configuracao_form.is_valid():
                configuracao = configuracao_form.save(commit=False)
                configuracao.analiseSolo = analise_solo  # Relacione com o AnaliseSolo

                # Preencha o AnaliseForm
                analise_form = AnaliseForm(request.POST)
                if analise_form.is_valid():
                    analise = analise_form.save(commit=False)
                    analise.analiseSolo = analise_solo  # Relacione com o AnaliseSolo
                    analise.save()

                    configuracao.analise = analise  # Relacione com o Analise
                    configuracao.save()

                    return redirect('alguma_pagina_de_sucesso')  # Redirecione para uma página de sucesso

    else:
        analise_solo_form = AnaliseSoloForm(user=request.user)
        configuracao_form = ConfiguracaoAlgoritmoForm()
        analise_form = AnaliseForm()

    return render(request, 'sua_template.html', {
        'analise_solo_form': analise_solo_form,
        'configuracao_form': configuracao_form,
        'analise_form': analise_form,
    })


def roda_analise_solo(request):

    usuario = request.user.username
    data = timezone.now()

    # Crie uma instância de AnaliseSolo com os valores necessários
    nova_analise_solo = AnaliseSolo(usuario=usuario, data_analise=data)  # Supondo que você esteja usando o módulo timezone do Django para obter a data atual

    # Salve a instância no banco de dados
    nova_analise_solo.save()

def detalhes_analise_solo(request, analise_solo_id):
    # Suponha que você tenha recuperado a instância de AnaliseSolo com base no ID
    analise_solo = AnaliseSolo.objects.get(pk=analise_solo_id)
    
    return render(request, 'inserir_analise.html', {'analise_solo': analise_solo})
'''



