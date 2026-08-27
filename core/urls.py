from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import ping

urlpatterns = [
    # Endpoint de keepalive/healthcheck (usado pelo GitHub Actions e Render)
    path('ping/', ping, name='ping'),
    # O painel administrativo premium substituiu o Django Admin em /admin/
    path('admin/', RedirectView.as_view(pattern_name='painel:dashboard', permanent=False)),
    # Django Admin original fica disponível apenas em /django-admin/ (edição avançada)
    path('django-admin/', admin.site.urls),
    path('painel/', include('painel_admin.urls')),
    path('', include('users.urls')),
    path('cursos/', include('courses.urls')),
    path('gamificacao/', include('gamification.urls')),
    path('ia/', include('ia_engine.urls')),
    path('chat/', include('chat_devocional.urls')),
    path('quiz/', include('quiz_kahoot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
