from django.db import models

class Colheita(models.Model):
    nome_colheita = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_colheita
