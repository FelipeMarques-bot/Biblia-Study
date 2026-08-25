from django.contrib import admin
from .models import (
    Trilha, LicaoBiblica, Exercicio, ProgressoUsuario,
    ExercisePool, PerformanceTracker, GeneratedLesson,
)

@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'faixa_etaria', 'nivel', 'ordem', 'ativo']
    list_filter = ['faixa_etaria', 'nivel', 'ativo']

@admin.register(LicaoBiblica)
class LicaoBiblicaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'trilha', 'ordem', 'xp_recompensa']
    list_filter = ['trilha']

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ['enunciado', 'licao', 'tipo', 'ordem']

@admin.register(ProgressoUsuario)
class ProgressoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'licao', 'concluida', 'data_conclusao', 'xp_ganho_sessao']
    list_filter = ['concluida']

@admin.register(ExercisePool)
class ExercisePoolAdmin(admin.ModelAdmin):
    list_display = ['enunciado', 'tipo', 'topico', 'dificuldade', 'faixa_etaria', 'ativo', 'vezes_usado', 'taxa_acerto']
    list_filter = ['topico', 'dificuldade', 'faixa_etaria', 'ativo', 'tipo']
    search_fields = ['enunciado', 'referencia_biblica']

@admin.register(PerformanceTracker)
class PerformanceTrackerAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'topico', 'dificuldade', 'total_questoes', 'acertos', 'taxa_acerto', 'combo_maximo']
    list_filter = ['topico', 'dificuldade']

@admin.register(GeneratedLesson)
class GeneratedLessonAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'topico', 'dificuldade', 'concluida', 'xp_ganho', 'data_criacao']
    list_filter = ['topico', 'dificuldade', 'concluida']
    search_fields = ['titulo']
