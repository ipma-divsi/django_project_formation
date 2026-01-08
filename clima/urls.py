from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("mapa/", views.mapa, name="mapa"),
    path("aviso/<int:id>/", views.detalhe_aviso, name="detalhe_aviso"),
    path("mar/", views.mapa_mar, name="mapa_mar"),
    path("mar/praia/<int:id>/", views.detalhe_praia, name="detalhe_praia"),
     path("mar/", views.mapa_mar, name="mar"),

]


