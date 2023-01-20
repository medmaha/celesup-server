from django.contrib.auth.models import AnonymousUser

def profile(request):
    return []
    if isinstance(request.user, AnonymousUser):
        user = request.user.get_profile()
        return {'profile': user}