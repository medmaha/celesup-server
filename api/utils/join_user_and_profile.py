
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from celebrity.models import Celebrity
from supporter.models import Supporter
from utils.generators import get_user_profile


def get_profile_n_user_data(user, profile, user_type):
    """ Combines and return the user information \nalongside the corresponding profile information"""

    return_data = None
    user = User.objects.get(email=user.email)

    if user_type.lower().startswith('ce'):
        profile = Celebrity.objects.get(id=profile.id)
        return_data = True
    elif user_type.lower().startswith('su'):
        profile = Supporter.objects.get(id=profile.id)
        return_data = True

    if not return_data:
        return {}

    return_data = {
        'id': str(profile.id[:15]),
        'avater': str(profile.avater.url),
        'friends_count': str(profile.friends.count()),

        'username': str(user.username),
        'email': str(user.email),
        'first_name':  str(user.first_name),
        'last_name': str(user.last_name)
    }
    
    return return_data


def get_user_data_n_tokens(user):

    """
        Generates a new access and and refresh token from newly created user \n
        with a collection of user's information and the user_profile data
    """
    
    [profile, user_type] = get_user_profile(user).values()
    user_data = get_profile_n_user_data(user, profile, user_type)

    token = RefreshToken.for_user(user)
    user_tokens =  {'refresh': str(token), 'access': str(token.access_token)}

    return {'user': user_data, 'tokens':user_tokens}

