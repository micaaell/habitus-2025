from django.shortcuts import render

def login(request):
    return render(request, 'PagsUsuario/login.html')
def feed(request):
    return render(request, 'PagsUsuario/feed.html')
def treinos(request):
    return render(request, 'PagsUsuario/treinos.html')
def perfil(request):
    return render(request, 'PagsUsuario/perfil.html')
