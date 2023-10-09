from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
import pandas as pd
import tkinter as tk

df=pd.read_csv('crop.csv')
print(df.describe())

@login_required
def recomendar_colheita(request):
    return render(request, "recomendar_colheita.html")

def carregar_dados_csv():
    df=pd.read_csv('crop.csv')
    return df

def enviar_colheita(request):
    if request.method == 'POST':
        label_selecionado = request.POST['label']

        return label_selecionado
    
def calcular_media(request):
    if request.method == 'POST':
        label_selecionado = request.POST['label']

        # Lê o arquivo CSV
        df = pd.read_csv('crop.csv')

        # Filtra os dados com base no rótulo selecionado
        dados_filtrados = df[df['label'] == label_selecionado]

        # Calculando a média
        media_n = dados_filtrados['N'].mean()
        media_p = dados_filtrados['P'].mean()
        media_k = dados_filtrados['K'].mean()
        media_temperature = dados_filtrados['temperature'].mean()
        media_humidity = dados_filtrados['humidity'].mean()
        media_ph = dados_filtrados['ph'].mean()
        media_rainfall = dados_filtrados['rainfall'].mean()

        # Calculando o mínimo
        min_n = dados_filtrados['N'].min()
        min_p = dados_filtrados['P'].min()
        min_k = dados_filtrados['K'].min()
        min_temperature = dados_filtrados['temperature'].min()
        min_humidity = dados_filtrados['humidity'].min()
        min_ph = dados_filtrados['ph'].min()
        min_rainfall = dados_filtrados['rainfall'].min()

        # Calculando o máximo
        max_n = dados_filtrados['N'].max()
        max_p = dados_filtrados['P'].max()
        max_k = dados_filtrados['K'].max()
        max_temperature = dados_filtrados['temperature'].max()
        max_humidity = dados_filtrados['humidity'].max()
        max_ph = dados_filtrados['ph'].max()
        max_rainfall = dados_filtrados['rainfall'].max()

        # Calculando o desvio padrão
        std_n = dados_filtrados['N'].std()
        std_p = dados_filtrados['P'].std()
        std_k = dados_filtrados['K'].std()
        std_temperature = dados_filtrados['temperature'].std()
        std_humidity = dados_filtrados['humidity'].std()
        std_ph = dados_filtrados['ph'].std()
        std_rainfall = dados_filtrados['rainfall'].std()

        request.session['resultados'] = context

        context = {
        'colheita': label_selecionado,
        'media_n': round(media_n, 2),
        'media_p': round(media_p, 2),
        'media_k': round(media_k, 2),
        'media_temperature': round(media_temperature, 2),
        'media_humidity': round(media_humidity, 2),
        'media_ph': round(media_ph, 2),
        'media_rainfall': round(media_rainfall, 2),
        'min_n': round(min_n, 2),
        'min_p': round(min_p, 2),
        'min_k': round(min_k, 2),
        'min_temperature': round(min_temperature, 2),
        'min_humidity': round(min_humidity, 2),
        'min_ph': round(min_ph, 2),
        'min_rainfall': round(min_rainfall, 2),
        'max_n': round(max_n, 2),
        'max_p': round(max_p, 2),
        'max_k': round(max_k, 2),
        'max_temperature': round(max_temperature, 2),
        'max_humidity': round(max_humidity, 2),
        'max_ph': round(max_ph, 2),
        'max_rainfall': round(max_rainfall, 2),
        'std_n': round(std_n, 2),
        'std_p': round(std_p, 2),
        'std_k': round(std_k, 2),
        'std_temperature': round(std_temperature, 2),
        'std_humidity': round(std_humidity, 2),
        'std_ph': round(std_ph, 2),
        'std_rainfall': round(std_rainfall, 2),
}


        return render(request, 'recomendar_colheita.html', context)

from django.http import FileResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def gerar_relatorio_colheita(request):

    resultados = request.session.get('resultados', {})
    # Cria um buffer para armazenar o PDF em memória
    buffer = BytesIO()

    # Cria o PDF no buffer
    cnv = canvas.Canvas(buffer, pagesize=A4)
    #cnv  = canvas.Canvas("./relatorio/relatorio_colheita.pdf", pagesize=A4)
    cnv.setFont('Helvetica-Bold', 18)
    
    # Desenhar a imagem do cabeçalho (ajuste as coordenadas conforme necessário)
    #cnv.drawImage("cabecalho.png", 15, 770)

    # Adicionar texto (ajuste as coordenadas conforme necessário)
    cnv.drawString(35, 720, f"Colheita: {resultados.get('colheita', '')}")
    cnv.drawString(35, 690, "Media dos valores da colheita")

    cnv.setFont('Helvetica', 14)

    data = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ]

    media_x = 35
    media_y = 650

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data:
        for i, cell in enumerate(row):
            cnv.rect(media_x, media_y, col_widths[i], row_height)
            cnv.drawString(media_x + 5, media_y + 5, cell)
            media_x += col_widths[i]
        media_y -= row_height
        media_x = 35

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 600, "Valores mínimos do solo para a colheita")

    cnv.setFont('Helvetica', 14)

    min_x = 35
    min_y = 560

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data:
        for i, cell in enumerate(row):
            cnv.rect(min_x, min_y, col_widths[i], row_height)
            cnv.drawString(min_x + 5, min_y + 5, cell)
            min_x += col_widths[i]
        min_y -= row_height
        min_x = 35

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 510, "Valores maximos do solo para a colheita")

    cnv.setFont('Helvetica', 14)

    max_x = 35
    max_y = 470

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data:
        for i, cell in enumerate(row):
            cnv.rect(max_x, max_y, col_widths[i], row_height)
            cnv.drawString(max_x + 5, max_y + 5, cell)
            max_x += col_widths[i]
        max_y -= row_height
        max_x = 35
    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 420, "Desvio padrão para a colheita")

    cnv.setFont('Helvetica', 14)

    std_x = 35
    std_y = 380

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data:
        for i, cell in enumerate(row):
            cnv.rect(std_x, std_y, col_widths[i], row_height)
            cnv.drawString(std_x + 5, std_y + 5, cell)
            std_x += col_widths[i]
        std_y -= row_height
        std_x = 35
        
    cnv.showPage()
    cnv.save()

    # Move o ponteiro do buffer para o início
    buffer.seek(0)

    # Retorna o PDF como uma resposta HTTP
    response = FileResponse(buffer, as_attachment=True, filename="relatorio_colheita.pdf")
    del request.session['resultados']

    return response


