from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_join, name='quiz_join'),
    path('<str:pin>/', views.quiz_player, name='quiz_player'),
    path('<str:pin>/lobby/', views.quiz_lobby, name='quiz_lobby'),
    path('<str:pin>/host/', views.quiz_host, name='quiz_host'),
    path('<str:pin>/podio/', views.quiz_podium, name='quiz_podium'),
    # API
    path('<str:pin>/api/start/', views.api_start_game, name='quiz_api_start'),
    path('<str:pin>/api/next/', views.api_next_question, name='quiz_api_next'),
    path('<str:pin>/api/results/', views.api_show_results, name='quiz_api_results'),
    path('<str:pin>/api/answer/', views.api_submit_answer, name='quiz_api_answer'),
    path('<str:pin>/api/restart/', views.api_restart, name='quiz_api_restart'),
]
