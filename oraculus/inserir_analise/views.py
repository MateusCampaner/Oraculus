from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise

import numpy as np
import pandas as pd
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
import seaborn as sns
import matplotlib.pyplot as plt



@login_required
def inserir_analise(request):
    return render(request, "inserir_analise.html")

def inserir_dados_analise(request):
    dataset = [
        {'n': '', 'p': '', 'k': '', 'humidade': '', 'temperatura': '', 'ph': '', 'chuva': ''},
    ]

    return render(request, 'inserir_analise.html', {'dataset': dataset})

def post_inserir_analise(request):
    N = request.POST.get('N')
    P = request.POST.get('P')
    K = request.POST.get('K')
    Umidade = request.POST.get('Umidade')
    Temperatura = request.POST.get('Temperatura')
    pH = request.POST.get('pH')
    Chuva = request.POST.get('Chuva')
    
    Analise.objects.create(N=N, P=P, K=K, Umidade=Umidade, Temperatura=Temperatura, pH=pH, Chuva=Chuva)

    return render(request, 'acessar_dados.html')

def delete_inserir_analise(request, id):
    analise = Analise.objects.get(id=id)
    analise.delete()
    return render(request, 'acessar_dados.html')

# Leitura do csv
df=pd.read_csv('crop.csv')
df.head()

# Preparo da IA para entender os dados
c=df.label.astype('category')
targets = dict(enumerate(c.cat.categories))
df['target']=c.cat.codes

y=df.target
X=df[['N','P','K','temperature','humidity','ph','rainfall']]

# Preparar as escalas ph e rainfall
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1)

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

# Aplicar o modelo KNN
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)
knn.score(X_test_scaled, y_test)

# Função para fazer previsões com base nos dados inseridos manualmente
def fazer_previsao_knn(modelo, dados_de_entrada):

    dados_de_entrada_padronizados = scaler.transform(dados_de_entrada.reshape(1, -1))
    previsao = modelo.predict(dados_de_entrada_padronizados)
    colheita_prevista = targets.get(previsao[0])

    return colheita_prevista

dados_de_entrada_manual = np.array([90, 42, 43, 20, 82, 6.5, 202])


colheita_prevista = fazer_previsao_knn(knn, dados_de_entrada_manual)

print("Com base nos dados de solo inseridos, a melhor colheita recomendada é:", colheita_prevista)

#jogar o crud da analise aqui
