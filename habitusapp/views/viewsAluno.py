from django.shortcuts import render

def feed(request):
    return render(request, 'PagsAluno/feed.html')
def treinos(request):
    return render(request, 'PagsAluno/treinos.html')
def perfil(request):
    return render(request, 'PagsAluno/perfil.html')
