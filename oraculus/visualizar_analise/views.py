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

    buffer = BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)

    usuario = request.user

    cnv.setFont('Helvetica-Bold', 18)
    cnv.drawImage("./recomendar_colheita/relatorio/cabecalho.png", 15, 750)

    cnv.drawString(35, 720, f"Análise {1}")
    cnv.drawString(160, 720, f"Usuário: {usuario.username}")
    cnv.drawString(350, 720, f"Data: 00/00/0000")

    cnv.drawString(35, 690, "Colheita recomendada: Bosta")

    cnv.setFont('Helvetica', 14)

    data_media = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{00000}", f"{00000}", f"{00000}", f"{00000}", f"{00000}", f"{00000}", f"{00000}"],
    ]

    anal_x = 35
    anal_y = 650

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
    cnv.drawString(35, 600, "Score-Z dos valores da colheita")

    cnv.setFont('Helvetica', 14)

    data_media = [
        ["Nitrogênio", "Potássio", "Fósforo", "Temperatura", "Umidade", "pH", "Chuva"],
        [f"{00000}", f"{00000}", f"{00000}", f"{00000}", f"{00000}", f"{00000}", f"{00000}"],
    ]

    scoreZ_x = 35
    scoreZ_y = 560

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

    response = FileResponse(buffer, as_attachment=True, filename="analise.pdf")
    
    return response