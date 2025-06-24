from django.db import models

class Treino(models.Model):
    nome = models.CharField(max_length=100)
    quant_exercicios = models.IntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return self.nome
