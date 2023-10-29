from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@login_required
def resultado(request):
    return render(request, "resultado.html")

def get_analises(request):
    analises = Analise.objects.all()
    return render(request, 'resultado.html', {'analises': analises})



