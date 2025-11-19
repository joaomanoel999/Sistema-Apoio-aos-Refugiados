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



class Usuario(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário independente com login por telefone."""
    
    # Atributos principais
    telefone = models.CharField(max_length=15, unique=True, verbose_name=_('Telefone'))
    email = models.EmailField(_('endereço de email'), unique=True, blank=True, null=True)
    
  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups', # Nome único para evitar conflito
        related_query_name='usuario',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions', # Resolve o conflito E304
        related_query_name='usuario',
    )
    USERNAME_FIELD = 'telefone' 
    REQUIRED_FIELDS = []
    
    objects = UsuarioManager() 
    
    def __str__(self):
        return self.telefone
    


class StatusRefugio(models.TextChoices):
    SOLICITANTE = 'SOLICITANTE', 'Solicitante'
    RECONHECIDO = 'RECONHECIDO', 'Reconhecido'
    NEGADO = 'NEGADO', 'Negado'
    REGULARIZACAO = 'REGULARIZACAO', 'Em Regularização'
    OUTRO = 'OUTRO', 'Outro'


class Refugiado(models.Model):
    """ Contém dados de perfil do refugiado, ligado ao usuário customizado. """
 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE) 
    
    nome_completo = models.CharField(max_length=200, blank=False, null=False) 
    data_nascimento = models.DateField(blank=False, null=False)
    pais_origem = models.CharField(max_length=100, blank=False, null=False)
    idioma_nativo = models.CharField(max_length=50, blank=False, null=False) 
    
    status_refugio = models.CharField(
        max_length=15, 
        choices=StatusRefugio.choices, 
        default=StatusRefugio.SOLICITANTE
    )
    
 
    cep = models.CharField(max_length=9,default='' , blank=False, null=False)
    logradouro = models.CharField(max_length=255, default='' , blank=False, null=False)
    numero_endereco = models.CharField(max_length=10, default='' , blank=False, null=False)
    complemento = models.CharField(max_length=100, default='' , blank=True, null=True)
    bairro = models.CharField(max_length=100, default='' , blank=False, null=False)
    cidade = models.CharField(max_length=100,default='' , blank=False, null=False)
    estado = models.CharField(max_length=2, default='' , blank=False, null=False)
    
    def __str__(self):
        return f"Refugiado: {self.nome_completo}"


class Voluntario(models.Model):
    """ Contém dados de perfil do voluntário. """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE) 
    
  
    nome_completo = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(unique=True) 
    telefone = models.CharField(max_length=15, blank=False, null=False,default= "") 
    
   
    idiomas_falados = models.TextField(help_text="Lista de idiomas separados por vírgula", blank=False, null=False, default="")
    habilidades_oferecidas = models.TextField(help_text="Lista de habilidades separadas por vírgula", blank=False, null=False,default="")
    disponibilidade = models.TextField(blank=False, null=False, default="")
    localizacao = models.CharField(max_length=255, blank=False, null=False,default="")
    
    def __str__(self):
        return f"Voluntário: {self.nome_completo}"