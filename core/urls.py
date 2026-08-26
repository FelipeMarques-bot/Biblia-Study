from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('cursos/', include('courses.urls')),
    path('gamificacao/', include('gamification.urls')),
    path('ia/', include('ia_engine.urls')),
    path('chat/', include('chat_devocional.urls')),
    path('quiz/', include('quiz_kahoot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
