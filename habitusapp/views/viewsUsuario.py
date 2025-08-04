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


from django.contrib.auth.decorators import login_required
from habitusapp.models import Treino
from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from habitusapp.models import Treino, Notificacao

@login_required
def treinos(request):
    treinos_usuario = Treino.objects.filter(usuario=request.user).order_by('-id')

    return render(request, 'PagsUsuario/treinos.html', {
        'treinos_usuario': treinos_usuario,
    })


@login_required
def detalhes_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)
    return render(request, 'PagsUsuario/detalhes_treino.html', {'treino': treino})

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
        Notificacao.objects.create(
        usuario=request.user,
        conteudo="Você alterou sua foto de perfil"
        )

        return redirect('perfil')

    return render(request, 'PagsUsuario/perfil.html', {'perfil': perfil})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from habitusapp.models import Treino, TreinoExercicio, Exercicio
from django.utils import timezone
from datetime import datetime

@login_required
def novo_treino(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        nivel = request.POST.get('nivel')
        exercicios_ids = request.POST.getlist('exercicios')  # IDs dos exercícios
        series = request.POST.getlist('series')
        repeticoes = request.POST.getlist('repeticoes')
        carga = request.POST.getlist('carga')
        observacoes = request.POST.getlist('observacoes')

        # Conversão das datas
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

        treino = Treino.objects.create(
            nome=nome,
            data_inicio=data_inicio,
            data_fim=data_fim,
            nivel=nivel,
            quant_exercicios=len(exercicios_ids),
            usuario=request.user
        )
        Notificacao.objects.create(
            usuario=request.user,
            conteudo="Você criou um novo treino."
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



from django.http import JsonResponse
from habitusapp.models import Exercicio

def buscar_exercicios(request):
    termo = request.GET.get("q", "").strip().lower()
    exercicios = Exercicio.objects.filter(nome__icontains=termo)[:10]
    data = []
    for e in exercicios:
        data.append({
            "id": e.id,
            "nome": e.nome,
            "grupo_muscular": e.grupo_muscular,
            "video_url": e.video.url if e.video else None
        })
    return JsonResponse(data, safe=False)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from habitusapp.models import Notificacao

@login_required
def notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user)
    notificacoes.update(lida=True)  # marca todas como lidas
    return render(request, 'PagsUsuario/notificacoes.html', {'notificacoes': notificacoes})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from habitusapp.models import Treino

@login_required
def comecar_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)
    exercicios = list(treino.exercicios_treino.all())
    
    index = int(request.GET.get('ex', 0))  # pega o index atual
    if index < len(exercicios):
        exercicio_atual = exercicios[index]
    else:
        exercicio_atual = None  # acabou o treino

    return render(request, 'PagsUsuario/treino.html', {
        'treino': treino,
        'exercicio_atual': exercicio_atual,
        'proximo_index': index + 1,
        'total': len(exercicios)
    })

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from habitusapp.models import Treino

@login_required
def finalizar_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)

    # Diminui 1 do progresso geral se for maior que 0
    if treino.progresso_geral > 0:
        treino.progresso_geral -= 1
        treino.save()

    return HttpResponseRedirect(reverse('treinos'))


from django.db.models import Sum
from habitusapp.models import Treino

def calcular_progresso_usuario(usuario):
    treinos = Treino.objects.filter(usuario=usuario)
    total_treinos = treinos.count()
    soma_quant = treinos.aggregate(Sum('quant_treinos'))['quant_treinos__sum'] or 0

    if total_treinos > 0:
        progresso = round(soma_quant / total_treinos)

        # Atualiza todos os treinos com o novo valor
        treinos.update(progresso_geral=progresso)

        return progresso
    else:
        # Se não há treinos, zera todos
        treinos.update(progresso_geral=0)
        return 0



