from django.contrib import admin
from .models import Habilidade, Servico, SolicitacaoServico, VoluntarioHabilidade


admin.site.register(Habilidade)
admin.site.register(Servico)
admin.site.register(SolicitacaoServico)
admin.site.register(VoluntarioHabilidade)