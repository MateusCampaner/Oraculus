from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def inserir_analise(request):
    return render(request, "inserir_analise.html")

def inserir_dados_analise(request):
    dataset = [
        {'n': '', 'p': '', 'k': '', 'humidade': '', 'temperatura': '', 'ph': '', 'chuva': ''},
    ]

    return render(request, 'inserir_analise.html', {'dataset': dataset})