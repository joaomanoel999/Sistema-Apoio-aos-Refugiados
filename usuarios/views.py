# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView 
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.db import IntegrityError, transaction
from django.utils import timezone # Adicionado para garantir o fuso horário

# IMPORTAÇÃO DOS MODELOS DE DADOS
from .models import Refugiado, Voluntario 


def cadastro(request):
    # Verifica se o formulário foi enviado (requisição POST)
    if request.method == 'POST':
        
        # 1. IDENTIFICAÇÃO DO FORMULÁRIO E DADOS DE LOGIN
        
        # O Django verifica qual botão foi clicado, usando o campo 'nome_completo'
        if 'nome_completo' in request.POST and request.POST.get('nome_completo'):
            tipo_perfil = 'refugiado'
            username = request.POST['telefone'] 
        
        elif 'nome_completo_voluntario' in request.POST and request.POST.get('nome_completo_voluntario'):
            tipo_perfil = 'voluntario'
            # Voluntário usa o email como username
            username = request.POST['email_voluntario'] 
        
        else:
            return render(request, 'usuarios/cadastro.html', {'error': 'Formulário inválido.'})


        # Coleta dados comuns de autenticação (a senha é coletada do formulário correspondente)
        senha = request.POST.get('senha') or request.POST.get('senha_voluntario')
        nome_completo = request.POST.get('nome_completo') or request.POST.get('nome_completo_voluntario')
            
        try:
            # 2. CRIAÇÃO DO USUÁRIO BASE (SEGURANÇA DJANGO)
            # Usamos uma transação para garantir que, se a Etapa 3 falhar, a Etapa 2 seja desfeita.
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=senha,
                    first_name=nome_completo.split(' ')[0],
                    last_name=' '.join(nome_completo.split(' ')[1:])
                )

                # 3. CRIAÇÃO DO PERFIL ESTENDIDO (Refugiado ou Voluntário)
                if tipo_perfil == 'refugiado':
                    Refugiado.objects.create(
                        usuario=user, # Chave Estrangeira para o User
                        nome_completo=nome_completo, # 🌟 CORRIGIDO: Salva nome completo
                        data_nascimento=timezone.datetime.strptime(request.POST['data_nascimento'], '%d/%m/%Y').date(),
                        telefone=request.POST['telefone'],
                        pais_origem=request.POST['pais_origem'],
                        idioma_nativo=request.POST['idioma_nativo'],
                        status_refugio=request.POST['status_refugio'],
                        
                        # Endereço (usando .get() com valor padrão para campos não obrigatórios)
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
                        usuario=user, # Chave Estrangeira para o User
                        nome_completo=nome_completo, # 🌟 CORRIGIDO: Salva nome completo
                        email=request.POST['email_voluntario'],
                        telefone=request.POST['telefone_voluntario'],
                        idiomas_falados=idiomas_falados,
                        habilidades_oferecidas=habilidades_oferecidas,
                        disponibilidade=request.POST['disponibilidade'],
                        localizacao=request.POST['localizacao_voluntario'],
                    )
                
            # 4. AÇÃO PÓS-CADASTRO (Sucesso Total)
            return redirect('usuarios:login') 

        except IntegrityError:
            # Trata erro se o username (telefone/email) já existe (restrição UNIQUE)
            return render(request, 'usuarios/cadastro.html', {'error': 'Conta já existe. Tente fazer o login.'})
            
        except Exception as e:
            # Captura qualquer outro erro (como falha na conversão da Data ou KeyError)
            # Se a transação falhar, o User criado no Etapa 2 é desfeito (rollback)
            print(f"Erro inesperado no cadastro: {e}")
            return render(request, 'usuarios/cadastro.html', {'error': f'ERRO: Um campo é inválido ou obrigatório. Detalhes: {e}'})

    # Se a requisição for GET, apenas exibe o formulário
    return render(request, 'usuarios/cadastro.html')


class UsuarioLoginView(LoginView):
    # Usa a view de login nativa do Django para segurança
    template_name = 'usuarios/login.html' 
    success_url = '/servicos/'