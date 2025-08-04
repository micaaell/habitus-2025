from django.contrib.auth.models import User 
from django.db import models

class Treino(models.Model):
    NIVEIS = [
        ('I', 'Iniciante'),
        ('M', 'Intermediário'),
        ('A', 'Avançado'),
    ]
    
    nome = models.CharField(max_length=100)
    quant_exercicios = models.IntegerField(editable=False)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    nivel = models.CharField(max_length=1, choices=NIVEIS, default='I')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quant_treinos = models.IntegerField(editable=False, default=0)
    #progresso_geral = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.data_inicio and self.data_fim:
            delta = self.data_fim - self.data_inicio
            self.quant_treinos = max(delta.days + 1, 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
