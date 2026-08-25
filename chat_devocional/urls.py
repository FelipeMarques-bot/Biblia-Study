from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_devocional'),
    path('nova-sessao/', views.nova_sessao, name='nova_sessao'),
    path('<int:sessao_id>/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
    path('enviar/', views.enviar_mensagem, name='enviar_mensagem_nova'),
    path('devocional-hoje/', views.devocional_hoje, name='devocional_hoje'),
]
