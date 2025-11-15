# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView 
# 🌟 CORREÇÃO 1: Importar o SEU modelo customizado 'Usuario' 🌟
from .models import Usuario, Refugiado, Voluntario 
from django.contrib.auth import login as auth_login
from django.db import IntegrityError, transaction
from django.utils import timezone 

def cadastro(request):
    if request.method == 'POST':
        
        # 1. IDENTIFICAÇÃO DO FORMULÁRIO E DADOS DE LOGIN
        if 'nome_completo' in request.POST and request.POST.get('nome_completo'):
            tipo_perfil = 'refugiado'
            # Dados do Refugiado (Telefone é o login principal)
            telefone = request.POST['telefone']
            email = None # Refugiado não tem campo email
        
        elif 'nome_completo_voluntario' in request.POST and request.POST.get('nome_completo_voluntario'):
            tipo_perfil = 'voluntario'
            # Dados do Voluntário (Email é o identificador, Telefone é o login principal)
            telefone = request.POST['telefone_voluntario']
            email = request.POST['email_voluntario']
        
        else:
            return render(request, 'usuarios/cadastro.html', {'error': 'Formulário inválido.'})

        senha = request.POST.get('senha') or request.POST.get('senha_voluntario')
        nome_completo = request.POST.get('nome_completo') or request.POST.get('nome_completo_voluntario')
            
        try:
            with transaction.atomic():
                
                # 🌟 CORREÇÃO 2: Usar Usuario.objects.create_user 🌟
                # (Passa os campos corretos para o seu Modelo Customizado)
                
                user = Usuario.objects.create_user(
                    telefone=telefone, # Sempre passa o telefone (que é o USERNAME_FIELD)
                    email=email,       # Passa o email (ou None se for Refugiado)
                    password=senha
                )

                # 3. CRIAÇÃO DO PERFIL ESTENDIDO
                if tipo_perfil == 'refugiado':
                    Refugiado.objects.create(
                        usuario=user, 
                        nome_completo=nome_completo,
                        data_nascimento=timezone.datetime.strptime(request.POST['data_nascimento'], '%d/%m/%Y').date(),
                        # 🌟 CORREÇÃO 3: Removido 'telefone' (já está no modelo 'Usuario')
                        pais_origem=request.POST['pais_origem'],
                        idioma_nativo=request.POST['idioma_nativo'],
                        status_refugio=request.POST['status_refugio'],
                        
                        # Endereço
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
                
            # 4. AÇÃO PÓS-CADASTRO (Redireciona para o Login)
            return redirect('usuarios:login') 

        except IntegrityError:
            # Trata erro se o username (telefone/email) já existe (restrição UNIQUE)
            return render(request, 'usuarios/cadastro.html', {'error': 'Conta já existe. Tente fazer o login.'})
            
        except Exception as e:
            # Captura qualquer outro erro (como falha na conversão da Data ou KeyError)
            print(f"Erro inesperado no cadastro: {e}")
            return render(request, 'usuarios/cadastro.html', {'error': f'ERRO: Um campo é inválido ou obrigatório. Detalhes: {e}'})

    # Se a requisição for GET, apenas exibe o formulário
    return render(request, 'usuarios/cadastro.html')


class UsuarioLoginView(LoginView):
    # Usa a view de login nativa do Django para segurança
    template_name = 'usuarios/login.html' 
    success_url = '/servicos/catalogo.html' # URL de destino após o login