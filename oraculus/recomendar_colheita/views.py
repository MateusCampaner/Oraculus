from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


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
    
def calcular_valores(request):
    global context
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


def gerar_relatorio_colheita(request):
    
    buffer = BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)

    global context

    #cnv  = canvas.Canvas("./relatorio/relatorio_colheita.pdf", pagesize=A4)
    cnv.setFont('Helvetica-Bold', 18)
    #cnv.drawImage("cabecalho.png", 15, 770)

    colheita = context.get('colheita')

    # Adicionar texto (ajuste as coordenadas conforme necessário)
    cnv.drawString(35, 720, f"Colheita: {colheita}")
    cnv.drawString(35, 690, "Media dos valores da colheita")

    media_n = context.get('media_n')
    media_p = context.get('media_p')
    media_k = context.get('media_k')
    media_temperature = context.get('media_temperature')
    media_humidity = context.get('media_humidity')
    media_ph = context.get('media_ph')
    media_rainfall = context.get('media_rainfall')

    min_n = context.get('min_n')
    min_p = context.get('min_p')
    min_k = context.get('min_k')
    min_temperature = context.get('min_temperature')
    min_humidity = context.get('min_humidity')
    min_ph = context.get('min_ph')
    min_rainfall = context.get('min_rainfall')

    max_n = context.get('max_n')
    max_p = context.get('max_p')
    max_k = context.get('max_k')
    max_temperature = context.get('max_temperature')
    max_humidity = context.get('max_humidity')
    max_ph = context.get('max_ph')
    max_rainfall = context.get('max_rainfall')

    std_n = context.get('std_n')
    std_p = context.get('std_p')
    std_k = context.get('std_k')
    std_temperature = context.get('std_temperature')
    std_humidity = context.get('std_humidity')
    std_ph = context.get('std_ph')
    std_rainfall = context.get('std_rainfall')



    cnv.setFont('Helvetica', 14)

    data_media = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{media_n}", f"{media_p}", f"{media_k}", f"{media_temperature}", f"{media_humidity}", f"{media_ph}", f"{media_rainfall}"],
    ]

    media_x = 35
    media_y = 650

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data_media:
        for i, cell in enumerate(row):
            cnv.rect(media_x, media_y, col_widths[i], row_height)
            cnv.drawString(media_x + 5, media_y + 5, cell)
            media_x += col_widths[i]
        media_y -= row_height
        media_x = 35

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 600, "Valores mínimos do solo para a colheita")

    cnv.setFont('Helvetica', 14)

    data_min = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{min_n}", f"{min_p}", f"{min_k}", f"{min_temperature}", f"{min_humidity}", f"{min_ph}", f"{min_rainfall}"],
    ]   


    min_x = 35
    min_y = 560

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data_min:
        for i, cell in enumerate(row):
            cnv.rect(min_x, min_y, col_widths[i], row_height)
            cnv.drawString(min_x + 5, min_y + 5, cell)
            min_x += col_widths[i]
        min_y -= row_height
        min_x = 35

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 510, "Valores maximos do solo para a colheita")

    cnv.setFont('Helvetica', 14)

    data_max = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{max_n}", f"{max_p}", f"{max_k}", f"{max_temperature}", f"{max_humidity}", f"{max_ph}", f"{max_rainfall}"],
    ]


    max_x = 35
    max_y = 470

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data_max:
        for i, cell in enumerate(row):
            cnv.rect(max_x, max_y, col_widths[i], row_height)
            cnv.drawString(max_x + 5, max_y + 5, cell)
            max_x += col_widths[i]
        max_y -= row_height
        max_x = 35
    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 420, "Desvio padrão para a colheita")

    cnv.setFont('Helvetica', 14)

    data_std = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{std_n}", f"{std_p}", f"{std_k}", f"{std_temperature}", f"{std_humidity}", f"{std_ph}", f"{std_rainfall}"],
    ]

    std_x = 35
    std_y = 380

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data_std:
        for i, cell in enumerate(row):
            cnv.rect(std_x, std_y, col_widths[i], row_height)
            cnv.drawString(std_x + 5, std_y + 5, cell)
            std_x += col_widths[i]
        std_y -= row_height
        std_x = 35
        
    cnv.showPage()
    cnv.save()

    buffer.seek(0)

    response = FileResponse(buffer, as_attachment=True, filename=f"relatorio_colheita_{colheita}.pdf")
    
    return response


