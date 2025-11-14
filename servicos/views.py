# servicos/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

# O decorador @login_required garante que apenas usuários autenticados acessem
@login_required 
def catalogo(request):
    """
    View que exibe o catálogo de serviços (tela de destino pós-login).
    """
    # A view renderiza o template que está em templates/servicos/catalogo.html
    return render(request, 'servicos/catalogo.html')