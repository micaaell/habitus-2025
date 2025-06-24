from django.shortcuts import render, redirect
from habitusapp.forms import AlunoForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from habitusapp.models import Aluno

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

            # Verificar o grupo do usuário
            grupos = user.groups.values_list('name', flat=True)

            if 'Aluno' in grupos:
                return redirect('feed_aluno')  # Exemplo: uma URL chamada feed_aluno
            elif 'Professor' in grupos:
                return redirect('feed_professor')  # Exemplo: uma URL chamada feed_professor
            elif 'Admin' in grupos:
                return redirect('feed_admin')  # Exemplo: uma URL chamada feed_admin
            else:
                return render(request, 'PagsUsuario/login.html', {'erro': 'Usuário sem grupo definido.'})

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
def feed_aluno(request):
    return render(request, 'PagsUsuario/feed.html')

@login_required
def treinos_aluno(request):
    return render(request, 'PagsUsuario/treinos.html')

@login_required
def meus_dados(request):
    aluno = Aluno.objects.get(user=request.user)
    return render(request, 'PagsUsuario/meus_dados.html', {'aluno': aluno})


@login_required
def perfil_aluno(request):
    try:
        aluno = Aluno.objects.get(user=request.user)
    except Aluno.DoesNotExist:
        aluno = None  # Pode fazer um redirect ou uma mensagem de erro se quiser

    return render(request, 'PagsUsuario/perfil.html', {'aluno': aluno})


@login_required
def editar_foto_aluno(request):
    aluno = Aluno.objects.get(user=request.user)

    if request.method == 'POST' and 'nova_foto' in request.FILES:
        # Se já existir uma foto, apaga a antiga antes de salvar a nova
        if aluno.foto_perfil and os.path.isfile(aluno.foto_perfil.path):
            os.remove(aluno.foto_perfil.path)

        # Salva a nova foto
        aluno.foto_perfil = request.FILES['nova_foto']
        aluno.save()

        return redirect('perfil_aluno')  # Redireciona de volta ao perfil

    return render(request, 'PagsAluno/perfil.html', {'aluno': aluno})




