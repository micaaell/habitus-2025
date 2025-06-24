from django.shortcuts import render, redirect
from habitusapp.forms import AlunoForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from habitusapp.models import Admin
from django.conf import settings
import os
from habitusapp.models import Noticia, Admin, Professor
from habitusapp.forms import NoticiaForm

@login_required
def feed_admin(request):
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    return render(request, 'PagsAdmin/feed.html', {'noticias': noticias})


@login_required
def treinos_admin(request):
    return render(request, 'PagsAdmin/treinos.html')

@login_required
def perfil_admin(request):
    try:
        admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
        admin = None  # Ou redirecione para uma página de erro, se quiser

    return render(request, 'PagsAdmin/perfil.html', {'admin': admin})

@login_required
def editar_foto_admin(request):
    admin = Admin.objects.get(user=request.user)

    if request.method == 'POST' and 'nova_foto' in request.FILES:
        # Se já existir uma foto, apaga a antiga antes de salvar a nova
        if admin.foto_perfil and os.path.isfile(admin.foto_perfil.path):
            os.remove(admin.foto_perfil.path)

        # Salva a nova foto
        admin.foto_perfil = request.FILES['nova_foto']
        admin.save()

        return redirect('perfil_admin')  # Redireciona de volta ao perfil

    return render(request, 'PagsAdmin/perfil.html', {'admin': admin})

@login_required
def gerenciar_noticias(request):
    return render(request, 'PagsAdmin/gerenciar_noticias.html')

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
            return redirect('feed_admin')  # Ou outro feed que desejar
    else:
        form = NoticiaForm()

    return render(request, 'PagsAdmin/publicar_noticia.html', {'form': form})




