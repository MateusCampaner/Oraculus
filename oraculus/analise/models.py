from django.db import models
from django.contrib.auth.models import User

class ConfiguracaoAlgoritmo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    qtdTeste = models.FloatField()
    qtdVizinhos = models.IntegerField()
    algoritmo = models.CharField(max_length=15)
    pesos = models.CharField(max_length=15)
    acuracia = models.FloatField()
    data_analise = models.DateTimeField(auto_now_add=True)

class Analise(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    configuracao_algoritmo = models.ForeignKey(ConfiguracaoAlgoritmo, on_delete=models.CASCADE)
    N = models.IntegerField()
    P = models.IntegerField()
    K = models.IntegerField()
    Temperatura = models.FloatField()
    Umidade = models.FloatField()
    pH = models.FloatField()
    Chuva = models.FloatField()
    Colheita = models.CharField(max_length=50)
    data_analise = models.DateTimeField(auto_now_add=True)

