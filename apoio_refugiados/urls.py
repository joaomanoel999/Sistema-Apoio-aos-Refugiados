# apoio_refugiados/urls.py (O arquivo principal do projeto)

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect 

urlpatterns = [
    
    path('admin/', admin.site.urls), 

   
    path('', lambda request: redirect('usuarios:login'), name='home'),
    

    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    
    

]