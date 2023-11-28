from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise, ConfiguracaoAlgoritmo
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def resultado(request):
    return render(request, "resultado.html")

def get_analises(request):
    analises = Analise.objects.all()
    return render(request, 'resultado.html', {'analises': analises})

def salvar_analises(request):
    id_modelo = request.POST.get('id_modelo')
    username = request.POST.get('username')
    configuracao_algoritmo = request.POST.get('id_modelo')
    N = request.POST.get('N')
    P = request.POST.get('P')
    K = request.POST.get('K')
    Temperatura = request.POST.get('Temperatura')
    Umidade = request.POST.get('Umidade')
    pH = request.POST.get('pH')
    Chuva = request.POST.get('Chuva')
    Colheita = request.POST.get('colheita_prevista')

    usuario = User.objects.filter(username=username).first()

    Temperatura = float(Temperatura.replace(',', '.'))
    Umidade = float(Umidade.replace(',', '.'))
    pH = float(pH.replace(',', '.'))
    Chuva = float(Chuva.replace(',', '.'))

    if id_modelo == "Padrão":
        id_modelo = 1

    configuracao_algoritmo = ConfiguracaoAlgoritmo.objects.get(id=id_modelo)

    resultado_analise = Analise(
        N=N,
        P=P,
        K=K,     
        Temperatura=Temperatura,
        Umidade=Umidade,
        pH=pH,
        Chuva=Chuva,
        Colheita=Colheita,
        usuario=usuario,
        configuracao_algoritmo=configuracao_algoritmo,
    )

    resultado_analise.save()

    messages.success(request, "Análise salva com sucesso")

    return redirect(resultado)



