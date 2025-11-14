
from django.urls import path
from . import views  
from .views import UsuarioLoginView 

app_name = 'usuarios'

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    
    path('cadastro/', views.cadastro, name='cadastro'),
]