from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Noticia(models.Model):
    class CategoriaChoices(models.TextChoices):
        AVISO_IMPORTANTE = 'AVISO IMPORTANTE', 'Aviso Importante'
        INFORMACAO = 'INFORMAÇÃO', 'Informação'
        OUTRO = 'OUTRO', 'Outro'

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_publicacao = models.DateTimeField(default=datetime.now)
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaChoices.choices,
        default=CategoriaChoices.INFORMACAO
    )

    autor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    autor_nome = models.CharField(max_length=100)
    autor_tipo = models.CharField(max_length=50)
    
    imagem = models.ImageField(upload_to='noticias/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor_nome}"
