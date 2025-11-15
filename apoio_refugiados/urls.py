# apoio_refugiados/urls.py

from django.contrib import admin
from django.urls import path, include # Garanta que 'include' está importado
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('usuarios:login'), name='home'),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    
    # 🌟 ADICIONE ESTA LINHA 🌟
    # Conecta o caminho /servicos/ ao arquivo servicos/urls.py
    path('servicos/', include('servicos.urls', namespace='servicos')), 
]