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
from django.db.models import Q

@login_required
def professores(request):
    busca = request.GET.get('busca', '')

    professores = Professor.objects.all()

    if busca:
        professores = professores.filter(
            Q(nome__icontains=busca) | Q(matricula__icontains=busca)
        )

    professores = professores.order_by('-data_criacao')

    context = {
        'professores': professores,
        'busca': busca,
    }
    return render(request, 'PagsAdmin/professores.html', context)


@login_required
def novo_professor(request):
    return render(request, 'PagsAdmin/novo_professor.html')

@login_required
def professor(request):
    return render(request, 'PagsAdmin/professor.html')



