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




