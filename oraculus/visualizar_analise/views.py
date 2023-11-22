from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise
from acessar_dados.views import acessar_dados
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

@login_required
def visualizar_analise(request, id):
    analises = Analise.objects.get(id=id)
    return render(request, "visualizar_analise.html")

def delete_analise(request, id):
    analises = Analise.objects.get(id=id)
    analises.delete()
    return redirect(acessar_dados)

def gerar_relatorio_analise(request):
    id = request.POST.get('id')
    username = request.POST.get('username')
    data_analise = request.POST.get('data_analise')
    N = request.POST.get('N')
    P = request.POST.get('P')
    K = request.POST.get('K')
    Temperatura = request.POST.get('Temperatura')
    Umidade = request.POST.get('Umidade')
    pH = request.POST.get('pH')
    Chuva = request.POST.get('Chuva')
    Colheita = request.POST.get('colheita_prevista')
    scoreZ_n = request.POST.get('scoreZ_n')
    scoreZ_p = request.POST.get('scoreZ_p')
    scoreZ_k = request.POST.get('scoreZ_k')
    scoreZ_temperature = request.POST.get('scoreZ_temperature')
    scoreZ_humidity = request.POST.get('scoreZ_humidity')
    scoreZ_ph = request.POST.get('scoreZ_ph')
    scoreZ_rainfall = request.POST.get('scoreZ_rainfall')

    buffer = BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawImage("./recomendar_colheita/relatorio/cabecalho.png", 15, 750)

    cnv.drawString(35, 720, f"Análise {id}")
    cnv.drawString(160, 720, f"Usuário: {username}")
    cnv.drawString(35, 690, f"Data: {data_analise}")

    cnv.drawString(35, 650, f"Colheita recomendada: {Colheita}")

    cnv.setFont('Helvetica', 14)

    data_media = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{N}", f"{P}", f"{K}", f"{Temperatura}", f"{Umidade}", f"{pH}", f"{Chuva}"],
    ]

    anal_x = 35
    anal_y = 610

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data_media:
        for i, cell in enumerate(row):
            cnv.rect(anal_x, anal_y, col_widths[i], row_height)
            cnv.drawString(anal_x + 5, anal_y + 5, cell)
            anal_x += col_widths[i]
        anal_y -= row_height
        anal_x = 35

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawString(35, 560, "Score-Z dos valores da colheita")

    cnv.setFont('Helvetica', 14)

    data_media = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{scoreZ_n}", f"{scoreZ_p}", f"{scoreZ_k}", f"{scoreZ_temperature}", f"{scoreZ_humidity}", f"{scoreZ_ph}", f"{scoreZ_rainfall}"],
    ]

    scoreZ_x = 35
    scoreZ_y = 520

    col_widths = [72, 72, 72, 90, 72, 72, 72]

    row_height = 20

    for row in data_media:
        for i, cell in enumerate(row):
            cnv.rect(scoreZ_x, scoreZ_y, col_widths[i], row_height)
            cnv.drawString(scoreZ_x + 5, scoreZ_y + 5, cell)
            scoreZ_x += col_widths[i]
        scoreZ_y -= row_height
        scoreZ_x = 35

    cnv.showPage()
    cnv.save()

    buffer.seek(0)

    response = FileResponse(buffer, as_attachment=True, filename=f"analise_{id}.pdf")
    
    return response