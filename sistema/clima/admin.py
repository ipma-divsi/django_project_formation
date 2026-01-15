from django.contrib import admin
from .models import AvisoMeteorologico, AvisoMar, Comentario, Praia, Noticia


@admin.register(AvisoMeteorologico)
class AvisoMeteorologicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel', 'data')
    list_filter = ('nivel',)
    search_fields = ('titulo', 'descricao')


@admin.register(AvisoMar)
class AvisoMarAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel', 'data')
    list_filter = ('nivel',)
    search_fields = ('titulo', 'descricao')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'aviso', 'data')
    search_fields = ('nome', 'texto')


@admin.register(Praia)
class PraiaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'lat',
        'lon',
        
    )
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data')
    list_filter = ('data',)
    search_fields = ('titulo', 'descricao')
    ordering = ('-data',)