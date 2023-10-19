from recomendar_colheita.views import recomendar_colheita, enviar_colheita, calcular_media
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

cnv  = canvas.Canvas("./relatorio/relatorio_colheita.pdf", pagesize=A4)
cnv.setFont('Helvetica-Bold', 18)

cnv.drawImage("./relatorio/cabecalho.png", 15, 740)

cnv.drawString(35, 720, "Colheita: ")

cnv.drawString(200, 200, "Tester")

cnv.save()