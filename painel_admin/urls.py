from django.urls import path
from . import views

app_name = 'painel'

urlpatterns = [
    path('login/', views.painel_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/exportar.csv', views.exportar_usuarios_csv, name='exportar_usuarios'),
    path('usuarios/<int:user_id>/', views.usuario_detalhe, name='usuario_detalhe'),
    path('atividades/', views.atividades, name='atividades'),
    path('ranking/', views.ranking, name='ranking'),
    path('conteudo/trilhas/', views.trilhas, name='trilhas'),
    path('conteudo/licoes/', views.licoes, name='licoes'),
    path('conteudo/desafios/', views.desafios, name='desafios'),
    path('conteudo/recompensas/', views.recompensas, name='recompensas'),
]