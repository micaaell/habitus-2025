"""
URL configuration for devadmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from habitusapp.views.viewsUsuario import *
from habitusapp.views.viewsAdmin import *
from habitusapp.views.viewsProfessor import *
from habitusapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    #Páginas Usuário
    path('', login, name='login'),
    path('criar_conta/', criar_conta, name='criar_conta'),
    path('feed/', viewsUsuario.feed, name='feed'),
    path('treinos/', viewsUsuario.treinos, name='treinos'),
    path('perfil/', viewsUsuario.perfil, name='perfil'),
    path('perfil/editar-foto', viewsUsuario.editar_foto, name='editar_foto'),
    path('meus_dados/', viewsUsuario.meus_dados, name='meus_dados'),
    path('novo_treino/', viewsUsuario.novo_treino, name='novo_treino'),
    path('buscar-exercicios/', viewsUsuario.buscar_exercicios, name='buscar_exercicios'),

    #Páginas Professor
    path('gerenciar_noticias/', viewsProfessor.gerenciar_noticias, name='gerenciar_noticias'),
    path('publicar_noticia/', viewsProfessor.publicar_noticia, name='publicar_noticia'),

    #Páginas Admin
    path('professores/', viewsAdmin.professores, name='professores'),
    path('novo-professor/', viewsAdmin.novo_professor, name='novo_professor'),
    path('professor/', viewsAdmin.professor, name='professor'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
