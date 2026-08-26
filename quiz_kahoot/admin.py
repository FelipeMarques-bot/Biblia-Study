from django.contrib import admin
from .models import QuizRoom, QuizPlayer, QuizQuestion


class QuizPlayerInline(admin.TabularInline):
    model = QuizPlayer
    extra = 0
    readonly_fields = ['pontuacao', 'streak', 'max_streak', 'joined_at']


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0
    readonly_fields = ['pergunta', 'opcoes', 'correta_idx', 'tipo']


@admin.register(QuizRoom)
class QuizRoomAdmin(admin.ModelAdmin):
    list_display = ['pin', 'status', 'host_user', 'current_question_index', 'created_at']
    list_filter = ['status']
    search_fields = ['pin']
    inlines = [QuizPlayerInline, QuizQuestionInline]


@admin.register(QuizPlayer)
class QuizPlayerAdmin(admin.ModelAdmin):
    list_display = ['nome', 'room', 'pontuacao', 'streak', 'max_streak', 'is_host']
    list_filter = ['is_host']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['room', 'ordem', 'tipo', 'pergunta', 'correta_idx']
