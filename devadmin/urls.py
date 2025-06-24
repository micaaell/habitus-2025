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
    path('feed_aluno/', viewsUsuario.feed_aluno, name='feed_aluno'),
    path('treinos_aluno/', viewsUsuario.treinos_aluno, name='treinos_aluno'),
    path('perfil_aluno/', viewsUsuario.perfil_aluno, name='perfil_aluno'),
    path('perfil_aluno/editar-foto', viewsUsuario.editar_foto_aluno, name='editar_foto_aluno'),
    path('meus_dados/', viewsUsuario.meus_dados, name='meus_dados'),

    #Páginas Professor
    path('feed_professor/', viewsProfessor.feed_professor, name='feed_professor'),
    path('treinos_professor/', viewsProfessor.treinos_professor, name='treinos_professor'),
    path('perfil_professor/', viewsProfessor.perfil_professor, name='perfil_professor'),
    path('perfil_professor/editar-foto', viewsProfessor.editar_foto_professor, name='editar_foto_professor'),

    #Páginas Admin
    path('feed_admin/', viewsAdmin.feed_admin, name='feed_admin'),
    path('treinos_admin/', viewsAdmin.treinos_admin, name='treinos_admin'),
    path('perfil_admin/', viewsAdmin.perfil_admin, name='perfil_admin'),
    path('perfil_admin/editar-foto', viewsAdmin.editar_foto_admin, name='editar_foto_admin'),
    path('gerenciar_noticias/', viewsAdmin.gerenciar_noticias, name='gerenciar_noticias'),
    path('publicar_noticia/', viewsAdmin.publicar_noticia, name='publicar_noticia'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
