from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_trilhas, name='lista_trilhas'),
    path('trilha/<int:trilha_id>/', views.mapa_trilha, name='mapa_trilha'),
    path('trilha/<int:trilha_id>/ir/', views.ir_para_trilha, name='ir_para_trilha'),
    path('licao/<int:licao_id>/', views.licao_view, name='licao'),
    path('licao/<int:licao_id>/verificar/', views.verificar_resposta, name='verificar_resposta'),
    path('licao/<int:licao_id>/finalizar/', views.finalizar_licao, name='finalizar_licao'),
    path('gerar-exercicios/', views.gerar_exercicios_ia, name='gerar_exercicios_ia'),
    path('gerar-licao/', views.gerar_licao_ia, name='gerar_licao_ia'),
    path('performance/', views.performance_view, name='performance_view'),
]
