from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise
from acessar_dados.views import acessar_dados

@login_required
def visualizar_analise(request):
    return render(request, "visualizar_analise.html")

def delete_analise(request, id):
    analises = Analise.objects.get(id=id)
    analises.delete()
    return redirect(acessar_dados)

