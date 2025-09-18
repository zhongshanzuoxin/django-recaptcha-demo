from django.conf import settings


def constant_text(request):
    content_name = getattr(settings, "CONTENT_NAME", {}) 
    return {
        'SERVICE_NAME': getattr(settings, "SERVICE_NAME", None),
        'DESCRIPTION': getattr(settings, "DESCRIPTION", None),


    }
