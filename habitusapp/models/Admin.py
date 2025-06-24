from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Admin(models.Model):
    class Tipo_Trabalho(models.TextChoices):
        ESTAGIO = 'Estágiario(a)', 'Estágiario(a)'
        EFETIVO = 'Professor(a)', 'Professor(a)'
        ADM = 'Administrador(a)', 'Administrador(a)'
    class NivelChoices(models.TextChoices):
        INICIANTE = 'Iniciante', 'Iniciante'
        INTERMEDIARIO = 'Intermediário', 'Intermediário'
        AVANCADO = 'Avançado', 'Avançado'
    class ObjetivoChoices(models.TextChoices):
        GANHODEMASSA = 'Ganho de Massa', 'Ganho de Massa'
        PERDADEPESO = 'Perda de peso', 'Perda de peso'
        SAUDE = 'Saúde', 'Saúde'
        OUTRO = 'Outro', 'Outro'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    foto_perfil = models.ImageField(null=True, blank=True, upload_to='foto-perfil-admin/')
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    data_nasc = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_admissao = models.DateField()
    tipo_trabalho = models.CharField(
        max_length=20,
        choices=Tipo_Trabalho.choices,
        blank=True, null=True
    )

    peso = models.FloatField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    nivel = models.CharField(
        max_length=20,
        choices=NivelChoices.choices,
        blank=True, null=True
    )
    objetivo = models.CharField(
        max_length=20,
        choices=ObjetivoChoices.choices,
        blank=True, null=True
    )

    #Medição das cincunfêrencias
    cintura = models.FloatField(blank=True, null=True)
    abdomen = models.FloatField(blank=True, null=True)
    torax = models.FloatField(blank=True, null=True)
    quadril = models.FloatField(blank=True, null=True)
    coxa_direita = models.FloatField(blank=True, null=True)
    coxa_esquerda = models.FloatField(blank=True, null=True)
    panturrilha_direita = models.FloatField(blank=True, null=True)
    panturrilha_esquerda = models.FloatField(blank=True, null=True)
    braco_direito = models.FloatField(blank=True, null=True)
    braco_esquerdo = models.FloatField(blank=True, null=True)

    #Medições das dobras cutâneas
    tricipital = models.FloatField(blank=True, null=True)
    subescapular = models.FloatField(blank=True, null=True)
    axilar_media = models.FloatField(blank=True, null=True)
    suprailiaca = models.FloatField(blank=True, null=True)
    abdominal = models.FloatField(blank=True, null=True)
    coxa = models.FloatField(blank=True, null=True)
    panturrilha= models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Geração automática da matrícula
        if not self.matricula:
            ano = date.today().year
            ultimo_admin_ano = Admin.objects.filter(matricula__startswith=str(ano)).count() + 1
            self.matricula = f"{ano}{str(ultimo_admin_ano).zfill(2)}"
        super().save(*args, **kwargs)

    @property
    def idade(self):
        today = date.today()
        idade = today.year - self.data_nasc.year - ((today.month, today.day) < (self.data_nasc.month, self.data_nasc.day))
        return idade

    def __str__(self):
        return f"{self.nome} ({self.matricula}) ({self.idade}) ({self.data_criacao})"
