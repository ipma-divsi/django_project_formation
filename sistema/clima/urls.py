from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("mapa/", views.mapa, name="mapa"),
    path('mapa/', views.mapa_mar, name='mapa_mar'),
   

    # AVISOS METEOROLÓGICOS (tempo)
    path("aviso/<int:id>/", views.detalhe_aviso, name="detalhe_aviso"),
    
    # MAR
    path("mar/", views.mapa_mar, name="mar"),
    path("mar/aviso/<int:id>/", views.detalhe_aviso_mar, name="detalhe_aviso_mar"),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/<int:id>/', views.detalhe_noticia, name='detalhe_noticia'),
    path("tempo/10-dias/", views.previsao_10_dias, name="previsao_10_dias"),
    path("tempo/descritiva/", views.previsao_descritiva, name="previsao_descritiva"),
    path("tempo/estacoes/", views.estacoes_online, name="estacoes_online"),

]
