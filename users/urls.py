from django.urls import path
from . import views
from . import dashboard_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('alterar-senha/', views.alterar_senha_view, name='alterar_senha'),
    path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
]
