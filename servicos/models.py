# servicos/models.py

from django.db import models
from usuarios.models import Refugiado, Voluntario 

# --- 1. MODELO: HABILIDADE ---
class Habilidade(models.Model):
    """ Define o tipo de ajuda oferecida. """
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome

# --- 2. MODELO: SERVICO (Catálogo - Relação 1:N com Habilidade) ---
class Servico(models.Model):
    """ Itens no catálogo que o refugiado pode solicitar. """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    habilidade_necessaria = models.ForeignKey(Habilidade, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.nome

# --- 3. MODELO: SOLICITACAO_SERVICO (Tabela de Ligação N:1) ---
class SolicitacaoServico(models.Model):
    """ Tabela que registra um pedido de ajuda feito por um refugiado. """
    refugiado = models.ForeignKey(Refugiado, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status_solicitacao = models.CharField(max_length=20, default='ABERTO')
    
    def __str__(self):
        return f"Solicitação {self.id} de {self.refugiado.usuario.telefone}"

# --- 4. MODELO: VOLUNTARIO_HABILIDADE (Tabela de Ligação N:M) ---
class VoluntarioHabilidade(models.Model):
    """ Tabela que registra a relação N:M entre Voluntário e Habilidade. """
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    habilidade = models.ForeignKey(Habilidade, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('voluntario', 'habilidade') 
        verbose_name_plural = "Habilidades Oferecidas (Voluntários)"
    
    def __str__(self):
        return f"{self.voluntario.nome_completo} oferece {self.habilidade.nome}"