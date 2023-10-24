from django.db import models
from django.contrib.auth.models import User 

class AnaliseSolo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_analise = models.DateField() 

class Analise(models.Model):
    N = models.IntegerField()
    P = models.IntegerField()
    K = models.IntegerField()
    Temperatura = models.FloatField()
    Umidade = models.FloatField()
    pH = models.FloatField()
    Chuva = models.FloatField()
    Colheita = models.CharField(max_length=50)
    analiseSolo = models.ForeignKey(AnaliseSolo, on_delete=models.CASCADE)

class ConfiguracaoAlgoritmo(models.Model):
    qtdTeste = models.FloatField()
    qtdVizinhos = models.IntegerField()
    algoritmo = models.CharField(max_length=15)
    pesos = models.CharField(max_length=15)
    acuracia = models.FloatField()
    analiseSolo = models.ForeignKey(AnaliseSolo, on_delete=models.CASCADE)
