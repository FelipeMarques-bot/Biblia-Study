from django.http import JsonResponse


def ping(request):
    """Endpoint leve para keepalive/healthcheck — não toca no banco."""
    return JsonResponse({'status': 'ok', 'app': 'biblia-study'})