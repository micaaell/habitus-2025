from django import forms
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.models import User, Group
from .models import Aluno

class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Usuário com esse e-mail não existe.')

        user = authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError('Email ou senha incorretos.')

        self.cleaned_data['user'] = user
        return self.cleaned_data

class AlunoForm(forms.ModelForm):
    username = forms.CharField(label='Nome de usuário')
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = Aluno
        fields = [
            'nome',
            'cpf',
            'data_nasc',
            'telefone',
            'foto_perfil'
        ]

    def save(self, commit=True):
        # Criar o usuário do Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        # Adicionar o user ao grupo "Aluno"
        grupo_aluno, created = Group.objects.get_or_create(name='Aluno')
        user.groups.add(grupo_aluno)

        # Criar o Aluno
        aluno = super().save(commit=False)
        aluno.user = user
        aluno.email = self.cleaned_data['email']  # Garantir que o email vai para o Aluno também
        if commit:
            aluno.save()
        return aluno

from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['imagem','categoria','descricao']

from django import forms
from .models import Treino

class TreinoForm(forms.ModelForm):
    class Meta:
        model = Treino
        fields = ['nome', 'nivel', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

