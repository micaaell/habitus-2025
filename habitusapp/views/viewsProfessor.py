from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from habitusapp.models import Professor
from django.conf import settings
import os

@login_required
def feed_professor(request):
    return render(request, 'PagsProfessor/feed.html')
    
@login_required
def treinos_professor(request):
    return render(request, 'PagsProfessor/treinos.html')

@login_required
def perfil_professor(request):
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        professor = None  # Ou você pode fazer um redirect

    return render(request, 'PagsProfessor/perfil.html', {'professor': professor})

@login_required
def editar_foto_professor(request):
    professor = Professor.objects.get(user=request.user)

    if request.method == 'POST' and 'nova_foto' in request.FILES:
        # Se já existir uma foto, apaga a antiga antes de salvar a nova
        if professor.foto_perfil and os.path.isfile(professor.foto_perfil.path):
            os.remove(professor.foto_perfil.path)

        # Salva a nova foto
        professor.foto_perfil = request.FILES['nova_foto']
        professor.save()

        return redirect('perfil_professor')  # Redireciona de volta ao perfil

    return render(request, 'PagsProfessor/perfil.html', {'professor': professor})

