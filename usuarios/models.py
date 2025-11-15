# usuarios/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# --- Gerenciador de Usuário Customizado (Obrigatorio para login por telefone) ---
class UsuarioManager(BaseUserManager):
    def create_user(self, telefone, password=None, **extra_fields):
        if not telefone:
            raise ValueError(_('O telefone é obrigatório para o cadastro'))
        
        user = self.model(telefone=telefone, **extra_fields)
        user.set_password(password) # Criptografa a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, telefone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # Omitido código de validação para brevidade
        return self.create_user(telefone, password, **extra_fields)

# --- CHOICES (Integridade de Domínio) ---
STATUS_REFUGIO_CHOICES = [
    ('SOLICITANTE', 'Solicitante'),
    ('RECONHECIDO', 'Reconhecido'),
    ('NEGADO', 'Negado'),
    ('REGULARIZACAO', 'Em Regularização'),
    ('OUTRO', 'Outro'),
]

# --- 1. MODELO: USUARIO (Tabela Customizada para Login por Telefone) ---
class Usuario(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário independente com login por telefone."""
    
    # Atributos principais
    telefone = models.CharField(max_length=15, unique=True, verbose_name=_('Telefone'))
    email = models.EmailField(_('endereço de email'), unique=True, blank=True, null=True)
    
    # Campos obrigatórios para o sistema de autenticação
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'telefone' 
    REQUIRED_FIELDS = []
    
    objects = UsuarioManager() 
    
    def __str__(self):
        return self.telefone

# --- 2. MODELO: REFUGIADO (Perfil 1:1) ---
class Refugiado(models.Model):
    """ Contém dados de perfil do refugiado, ligado ao usuário customizado. """
    # Integridade Referencial e Entidade
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE) 
    
    # Dados Pessoais
    nome_completo = models.CharField(max_length=200, default='') 
    data_nascimento = models.DateField()
    pais_origem = models.CharField(max_length=100)
    idioma_nativo = models.CharField(max_length=50) 
    
    status_refugio = models.CharField(
        max_length=15, 
        choices=STATUS_REFUGIO_CHOICES, 
        default='SOLICITANTE'
    )
    
    # Endereço (blank/null=True para campos opcionais no DB)
    cep = models.CharField(max_length=9, blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero_endereco = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    def __str__(self):
        return f"Refugiado: {self.nome_completo}"

# --- 3. MODELO: VOLUNTARIO (Perfil 1:1) ---
class Voluntario(models.Model):
    """ Contém dados de perfil do voluntário. """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE) 
    
    # Dados Pessoais
    nome_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True) 
    telefone = models.CharField(max_length=15, blank=True, null=True) 
    
    # Habilidades e Disponibilidade
    idiomas_falados = models.TextField(help_text="Lista de idiomas separados por vírgula", blank=True, null=True)
    habilidades_oferecidas = models.TextField(help_text="Lista de habilidades separadas por vírgula", blank=True, null=True)
    disponibilidade = models.TextField(blank=True, null=True)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Voluntário: {self.nome_completo}"