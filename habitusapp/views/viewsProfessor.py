from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from habitusapp.models import Professor
from django.conf import settings
import os

from django.shortcuts import render, redirect
from habitusapp.forms import AlunoForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from habitusapp.models import Admin
from django.conf import settings
from habitusapp.models import Noticia, Admin, Professor
from habitusapp.forms import NoticiaForm

@login_required
def gerenciar_noticias(request):
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    nome = None
    return render(request, 'PagsProfessor/gerenciar_noticias.html', {
        'noticias': noticias,
        'nome_usuario': nome
    })

@login_required
def publicar_noticia(request):
    nome_autor = ""
    tipo_autor = ""
    autor_user = request.user

    try:
        admin = Admin.objects.get(user=request.user)
        nome_autor = admin.nome
        tipo_autor = admin.tipo_trabalho
    except Admin.DoesNotExist:
        try:
            professor = Professor.objects.get(user=request.user)
            nome_autor = professor.nome
            tipo_autor = professor.tipo_trabalho
        except Professor.DoesNotExist:
            return redirect('erro_permissao')  # Opcional: criar uma página de erro caso o usuário não seja admin ou professor

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor_user = autor_user
            noticia.autor_nome = nome_autor
            noticia.autor_tipo = tipo_autor
            noticia.save()
            return redirect('feed')  # Ou outro feed que desejar
    else:
        form = NoticiaForm()

    return render(request, 'PagsProfessor/publicar_noticia.html', {'form': form})

