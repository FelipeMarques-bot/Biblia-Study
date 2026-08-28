from django.urls import path
from . import views

urlpatterns = [
    path('desafio-diario/', views.desafio_diario_view, name='desafio_diario'),
    path('desafio-diario/<int:desafio_id>/concluir/', views.concluir_desafio_diario, name='concluir_desafio'),
    path('recompensas/', views.recompensas_view, name='recompensas'),
    path('recompensas/<int:recompensa_id>/abrir/', views.abrir_bau, name='abrir_bau'),
    path('serie-ouro/', views.serie_ouro_view, name='serie_ouro'),
    path('serie-ouro/abrir-bau/', views.abrir_bau_divino, name='abrir_bau_divino'),
    path('serie-ouro/<int:desafio_id>/', views.serie_ouro_desafio_view, name='serie_ouro_desafio'),
    path('serie-ouro/<int:desafio_id>/verificar/', views.serie_ouro_verificar_view, name='serie_ouro_verificar'),
    path('serie-ouro/<int:desafio_id>/finalizar/', views.serie_ouro_finalizar_view, name='serie_ouro_finalizar'),
    path('ranking/', views.ranking_view, name='ranking'),
]
