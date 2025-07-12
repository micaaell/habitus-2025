from django.shortcuts import render, redirect
from habitusapp.forms import AlunoForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from habitusapp.forms import NoticiaForm
from habitusapp.models import Noticia, Aluno, Professor, Admin 

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'PagsUsuario/login.html', {'erro': 'Usuário com este e-mail não existe.'})

        user = authenticate(request, username=user_obj.username, password=senha)

        if user is not None:
            auth_login(request, user)
            return redirect('feed')  # Redireciona sempre para a view 'feed' após login
        else:
            return render(request, 'PagsUsuario/login.html', {'erro': 'Senha incorreta.'})

    return render(request, 'PagsUsuario/login.html')

def criar_conta(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AlunoForm()
    
    return render(request, 'PagsUsuario/criar_conta.html', {'form': form})

@login_required
def feed(request):
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    
    nome = None

    if hasattr(request.user, 'aluno'):
        nome = request.user.aluno.nome
    elif hasattr(request.user, 'professor'):
        nome = request.user.professor.nome
    elif hasattr(request.user, 'admin'):
        nome = request.user.admin.nome
    else:
        nome = request.user.username  # fallback, caso não esteja em nenhum perfil

    return render(request, 'PagsUsuario/feed.html', {
        'noticias': noticias,
        'nome_usuario': nome
    })


@login_required
def treinos(request):
    return render(request, 'PagsUsuario/treinos.html')

@login_required
def meus_dados(request):
    perfil = None

    if hasattr(request.user, 'aluno'):
        perfil = request.user.aluno
    elif hasattr(request.user, 'professor'):
        perfil = request.user.professor
    elif hasattr(request.user, 'admin'):
        perfil = request.user.admin

    return render(request, 'PagsUsuario/meus_dados.html', {'perfil': perfil})

@login_required
def perfil(request):
    perfil = None

    if hasattr(request.user, 'aluno'):
        perfil = request.user.aluno
    elif hasattr(request.user, 'professor'):
        perfil = request.user.professor
    elif hasattr(request.user, 'admin'):
        perfil = request.user.admin

    return render(request, 'PagsUsuario/perfil.html', {'perfil': perfil})

@login_required
def editar_foto(request):
    perfil = None

    if hasattr(request.user, 'aluno'):
        perfil = request.user.aluno
    elif hasattr(request.user, 'professor'):
        perfil = request.user.professor
    elif hasattr(request.user, 'admin'):
        perfil = request.user.admin

    if request.method == 'POST' and 'nova_foto' in request.FILES:
        # Remove a foto anterior (se houver)
        if perfil.foto_perfil and os.path.isfile(perfil.foto_perfil.path):
            os.remove(perfil.foto_perfil.path)

        perfil.foto_perfil = request.FILES['nova_foto']
        perfil.save()

        return redirect('perfil')

    return render(request, 'PagsUsuario/perfil.html', {'perfil': perfil})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from habitusapp.models import Treino, TreinoExercicio, Exercicio
from django.utils import timezone

@login_required
def novo_treino(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        exercicios_ids = request.POST.getlist('exercicios')  # IDs dos exercícios
        series = request.POST.getlist('series')
        repeticoes = request.POST.getlist('repeticoes')
        carga = request.POST.getlist('carga')
        observacoes = request.POST.getlist('observacoes')

        treino = Treino.objects.create(
            nome=nome,
            data_inicio=data_inicio,
            data_fim=data_fim,
            quant_exercicios=len(exercicios_ids),
            usuario=request.user
        )

        for i in range(len(exercicios_ids)):
            TreinoExercicio.objects.create(
                treino=treino,
                exercicio_id=exercicios_ids[i],
                series=series[i],
                repeticoes=repeticoes[i],
                carga=carga[i],
                observacao=observacoes[i]
            )

        return redirect('treinos')

    exercicios = Exercicio.objects.all()
    return render(request, 'PagsUsuario/novo_treino.html', {'exercicios': exercicios})






