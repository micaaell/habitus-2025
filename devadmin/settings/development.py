from .settings import*
import os
DEBUG = True
#Crie secret key para seu ambiente de desenvolvimento
SECRET_KEY='ixb62ha#ts=ab4t2u%p1_62-!5w2j==j6d^3-j$!z(@*m+-h'
ALLOWED_HOSTS = ['localhost','127.0.0.1','habitus-2025.onrender.com','habitus-cnat.vercel.app',]
DATABASES={
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}