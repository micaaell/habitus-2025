from django.shortcuts import render, redirect, get_object_or_404
from habitusapp.forms import AlunoForm, ProfessorForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from habitusapp.models import Admin
from django.contrib import messages
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
def professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    return render(request, 'PagsAdmin/professor.html', {'professor': professor})

@login_required
@require_POST
def atualizar_foto_professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    
    if 'foto' in request.FILES:
        # Remove a foto antiga se existir
        if professor.foto_perfil:
            professor.foto_perfil.delete(save=False)
        
        professor.foto_perfil = request.FILES['foto']
        professor.save()
        return JsonResponse({
            'success': True,
            'message': 'Foto atualizada com sucesso!',
            'foto_url': professor.foto_perfil.url
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Nenhuma foto foi selecionada.'
    }, status=400)

@login_required
def editar_professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor atualizado com sucesso!')
            return redirect('professor', pk=professor.pk)
    else:
        form = ProfessorForm(instance=professor)
    
    return render(request, 'PagsAdmin/editar_professor.html', {
        'professor': professor,
        'form': form
    })