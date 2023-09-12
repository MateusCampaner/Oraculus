from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import csv

@login_required
def recomendar_colheita(request):
    return render(request, "recomendar_colheita.html")

def calcular_media_tipo(colheita):
    colunas = [[] for _ in range(7)] 

    with open('crop.csv', 'r') as arquivo:
        leitor_csv = csv.reader(arquivo)
        next(leitor_csv)  

        for linha in leitor_csv:
            if len(linha) >= (8) and linha[7] == colheita:
                for i, valor in enumerate(linha[:7]):
                    colunas[i].append(float(valor))

    medias = [sum(coluna) / len(coluna) for coluna in colunas]

    return medias


def calcular_min_tipo(colheita):
    colunas = [[] for _ in range(7)] 

    with open('crop.csv', 'r') as arquivo:
        leitor_csv = csv.reader(arquivo)
        next(leitor_csv)  

        for linha in leitor_csv:
            if len(linha) >= (8) and linha[7] == colheita:
                for i, valor in enumerate(linha[:7]):
                    colunas[i].append(float(valor))

    minimos = [min(coluna) for coluna in colunas]

    return minimos

def calcular_max_tipo(colheita):
    colunas = [[] for _ in range(7)] 

    with open('crop.csv', 'r') as arquivo:
        leitor_csv = csv.reader(arquivo)
        next(leitor_csv)  

        for linha in leitor_csv:
            if len(linha) >= (8) and linha[7] == colheita:
                for i, valor in enumerate(linha[:7]):
                    colunas[i].append(float(valor))

    minimos = [max(coluna) for coluna in colunas]

    return minimos


