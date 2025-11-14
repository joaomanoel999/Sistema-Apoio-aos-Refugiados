# servicos/urls.py

from django.urls import path
from . import views 

# Define o namespace do app (crucial para o redirecionamento 'servicos:catalogo')
app_name = 'servicos'

urlpatterns = [
    # path('', ...) é a rota base, correspondente a /servicos/
    path('', views.catalogo, name='catalogo'),
]