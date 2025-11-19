# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView 
from .models import Usuario, Refugiado, Voluntario 
from django.contrib.auth import login as auth_login
from django.db import IntegrityError, transaction
from django.utils import timezone 

def cadastro(request):
    if request.method == 'POST':
        
        # 1. IDENTIFICAÇÃO DO FORMULÁRIO E DADOS DE LOGIN
        if 'nome_completo' in request.POST and request.POST.get('nome_completo'):
            tipo_perfil = 'refugiado'
        
            telefone = request.POST['telefone']
            email = None 
        
        elif 'nome_completo_voluntario' in request.POST and request.POST.get('nome_completo_voluntario'):
            tipo_perfil = 'voluntario'
            
            telefone = request.POST['telefone_voluntario']
            email = request.POST['email_voluntario']
        
        else:
            return render(request, 'usuarios/cadastro.html', {'error': 'Formulário inválido.'})

        senha = request.POST.get('senha') or request.POST.get('senha_voluntario')
        nome_completo = request.POST.get('nome_completo') or request.POST.get('nome_completo_voluntario')
            
        try:
            with transaction.atomic():
                
               
                
                user = Usuario.objects.create_user(
                    telefone=telefone, 
                    email=email,       
                    password=senha
                )

                # 3. CRIAÇÃO DO PERFIL ESTENDIDO
                if tipo_perfil == 'refugiado':
                    Refugiado.objects.create(
                        usuario=user, 
                        nome_completo=nome_completo,
                        data_nascimento=timezone.datetime.strptime(request.POST['data_nascimento'], '%d/%m/%Y').date(),
                        pais_origem=request.POST['pais_origem'],
                        idioma_nativo=request.POST['idioma_nativo'],
                        status_refugio=request.POST['status_refugio'],
                        
                        
                        cep=request.POST.get('cep', ''),
                        logradouro=request.POST.get('logradouro', ''),
                        numero_endereco=request.POST.get('numero_endereco', ''),
                        complemento=request.POST.get('complemento', ''),
                        bairro=request.POST.get('bairro', ''),
                        cidade=request.POST.get('cidade', ''),
                        estado=request.POST.get('estado', ''),
                    )
                
                else: # Voluntário
                    idiomas_falados = ",".join(request.POST.getlist('idiomas'))
                    habilidades_oferecidas = ",".join(request.POST.getlist('habilidades'))
                    
                    Voluntario.objects.create(
                        usuario=user, 
                        nome_completo=nome_completo, 
                        email=request.POST['email_voluntario'],
                        telefone=request.POST['telefone_voluntario'],
                        idiomas_falados=idiomas_falados,
                        habilidades_oferecidas=habilidades_oferecidas,
                        disponibilidade=request.POST['disponibilidade'],
                        localizacao=request.POST['localizacao_voluntario'],
                    )
                
           
            return redirect('usuarios:login') 

        except IntegrityError:
            return render(request, 'usuarios/cadastro.html', {'error': 'Conta já existe. Tente fazer o login.'})
            
        except Exception as e:
         
            print(f"Erro inesperado no cadastro: {e}")
            return render(request, 'usuarios/cadastro.html', {'error': f'ERRO: Um campo é inválido ou obrigatório. Detalhes: {e}'})

    # Se a requisição for GET, apenas exibe o formulário
    return render(request, 'usuarios/cadastro.html')


class UsuarioLoginView(LoginView): # HERDA
   
    template_name = 'usuarios/login.html' 
    success_url = '/servicos/catalogo.html' 