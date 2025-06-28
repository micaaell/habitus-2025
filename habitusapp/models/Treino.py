from django.contrib.auth.models import User
from django.db import models

class Treino(models.Model):
    nome = models.CharField(max_length=100)
    quant_exercicios = models.IntegerField(editable=False)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o usuário

    def __str__(self):
        return self.nome
