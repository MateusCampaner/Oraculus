from django.db import models

class Analise(models.Model):
    N = models.IntegerField()
    P = models.IntegerField()
    K = models.IntegerField()
    Temperatura = models.FloatField()
    Umidade = models.FloatField()
    pH = models.FloatField()
    Chuva = models.FloatField()


