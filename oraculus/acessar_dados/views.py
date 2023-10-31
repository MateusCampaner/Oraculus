from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise, ConfiguracaoAlgoritmo

@login_required
def acessar_dados(request):
    return render(request, "acessar_dados.html")

def acessar_dados_analise(request):
    analises = Analise.objects.all()
    return render(request, "acessar_dados_analise.html", {'analises': analises})

def acessar_dados_modelo(request):
    modelos = ConfiguracaoAlgoritmo.objects.all()
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
    return render(request, 'visualizar_analise.html', {'analises': analises})

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
