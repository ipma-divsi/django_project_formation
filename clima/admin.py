from django.contrib import admin
from .models import AvisoMeteorologico, Comentario, Praia, AvisoMar


@admin.register(AvisoMeteorologico)
class AvisoMeteorologicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'nivel', 'data')
    list_filter = ('tipo', 'nivel')
    search_fields = ('titulo', 'descricao')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'aviso', 'data')
    search_fields = ('nome', 'texto')


@admin.register(Praia)
class PraiaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'altura_onda',
        'direcao_onda',
        'temp_agua',
    )

@admin.register(AvisoMar)
class AvisoMarAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel', 'data')  # removi 'tipo'
    list_filter = ('nivel',)                    # removi 'tipo'
    search_fields = ('titulo', 'descricao')
 
