from django.urls import path
from .views import (
    home, login_view, dashboard, logout_view, register_view,
    editar_observacao, deletar_observacao, feed, minhas_observacoes,
    perfil, mapa
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('dashboard/', dashboard, name='dashboard'),

    # Minhas observações (CRUD)
    path('minhas-observacoes/', minhas_observacoes, name='minhas_observacoes'),
    path('editar/<int:pk>/', editar_observacao, name='editar_observacao'),
    path('deletar/<int:pk>/', deletar_observacao, name='deletar_observacao'),

    # Feed global
    path('feed/', feed, name='feed'),

    # Perfil do usuário
    path('perfil/', perfil, name='perfil'),
    # Mapa com observações
    path('mapa/', mapa, name='mapa'),
]
