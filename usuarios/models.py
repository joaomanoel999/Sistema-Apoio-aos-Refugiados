# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User


STATUS_REFUGIO_CHOICES = [
    ('SOLICITANTE', 'Solicitante'),
    ('RECONHECIDO', 'Reconhecido'),
    ('NEGADO', 'Negado'),
    ('REGULARIZACAO', 'Em Regularização'),
    ('OUTRO', 'Outro'),
]


class Refugiado(models.Model):
    """ Contém dados de perfil do refugiado, ligado ao usuário de autenticação. """
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) 
    
 
    nome_completo = models.CharField(max_length=200, null=False) 
    data_nascimento = models.DateField(null=False)
    telefone = models.CharField(max_length=15, unique=True, null=False) 
    pais_origem = models.CharField(max_length=100, null=False)
    idioma_nativo = models.CharField(max_length=50, null=False) 
    
    status_refugio = models.CharField(
        max_length=15, 
        choices=STATUS_REFUGIO_CHOICES, 
        default='SOLICITANTE'
    )
    
   
    cep = models.CharField(max_length=9, blank=True, null=False)
    logradouro = models.CharField(max_length=255, blank=True, null=False)
    numero_endereco = models.CharField(max_length=10, blank=True, null=False)
    complemento = models.CharField(max_length=100, blank=True, null=False)
    bairro = models.CharField(max_length=100, blank=True, null=False)
    cidade = models.CharField(max_length=100, blank=True, null=False)
    estado = models.CharField(max_length=2, blank=True, null=False)
    
    def __str__(self):
        return f"Refugiado: {self.nome_completo}"

#
class Voluntario(models.Model):
    """ Contém dados de perfil do voluntário. """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) 
    
   
    nome_completo = models.CharField(max_length=200, null=False) 
    email = models.EmailField(unique=True, null=False) 
    telefone = models.CharField(max_length=15, blank=True, null=False) 
    
   
    idiomas_falados = models.TextField(help_text="Lista de idiomas separados por vírgula", blank=True, null=False)
    habilidades_oferecidas = models.TextField(help_text="Lista de habilidades separadas por vírgula", blank=True, null=False)
    disponibilidade = models.TextField(blank=True, null=False)
    localizacao = models.CharField(max_length=255, blank=True, null=False)
    
    def __str__(self):
        return f"Voluntário: {self.nome_completo}"