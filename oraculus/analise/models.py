from django.db import models
from django.contrib.auth.models import User 

class Analise(models.Model):
    N = models.IntegerField()
    P = models.IntegerField()
    K = models.IntegerField()
    Temperatura = models.FloatField()
    Umidade = models.FloatField()
    pH = models.FloatField()
    Chuva = models.FloatField()
    Colheita = models.CharField(max_length=50)

class AnaliseSolo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    analise = models.ForeignKey(Analise, on_delete=models.CASCADE)
    data_analise = models.DateField() 


