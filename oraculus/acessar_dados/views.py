from django.shortcuts import render
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