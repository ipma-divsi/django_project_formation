from django.urls import path
from . import views

app_name = "clima"

urlpatterns = [
    path("", views.index, name="clima"),
    path("mapa/", views.mapa, name="mapa"),
    path('mapa_mar/', views.mapa_mar, name='mapa_mar'),
    # AVISOS METEOROLÓGICOS (tempo)
    path("aviso/<int:id>/", views.detalhe_aviso, name="detalhe_aviso"),

    # MAR
    path("mar/", views.mapa_mar, name="mar"),
    path("mar/aviso/<int:id>/", views.detalhe_aviso_mar, name="detalhe_aviso_mar"),
    path("mar/praia/<int:id>/", views.detalhe_praia, name="detalhe_praia"),
]
