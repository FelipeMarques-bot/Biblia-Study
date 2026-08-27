from django.contrib.auth.models import User


def painel_globals(request):
    """Expõe dados globais para a sidebar do painel (apenas para staff)."""
    ctx = {}
    if request.user.is_authenticated and request.user.is_staff:
        ctx['painel_total_usuarios'] = User.objects.filter(is_active=True).count()
    return ctx