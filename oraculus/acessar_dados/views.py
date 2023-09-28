from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise

@login_required
def acessar_dados(request):
    analises = Analise.objects.all()
    return render(request, "acessar_dados.html", {'analises': analises})

def get_analises(request):
    analises = Analise.objects.all()
    return render(request, 'acessar_dados.html', {'analises': analises})

def delete_analises(request, id):
    analises = Analise.objects.get(id=id)
    analises.delete()
    return redirect(acessar_dados)

def visualizar_analise(request, id):
    analises = Analise.objects.get(id=id)
    return render(request, 'visualizar_analise.html', {'analises': analises})
