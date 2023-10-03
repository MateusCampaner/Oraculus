from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
import pandas as pd

df=pd.read_csv('crop.csv')
print(df.describe())

@login_required
def recomendar_colheita(request):
    return render(request, "recomendar_colheita.html")

def carregar_dados_csv():
    df=pd.read_csv('crop.csv')
    return df

    



