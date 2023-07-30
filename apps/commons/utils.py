import re
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher

User = get_user_model()


def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


def authenticate_user(password, username=None, email=None):
    if not username and not email:
        return
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return
    else:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
    hasher = PBKDF2PasswordHasher()
    return user if hasher.verify(password, user.password) else None


def get_random_key(size):
    alphabets = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    random_key = ""
    for i in range(size):
        random_key += random.choice(alphabets)
    return random_key


def get_base_url(request):
    return "".join([f'{request.scheme}://', f'{request.get_host()}/'])


def is_profile_complete(user):
    try:
        profile = user.userprofile
    except:
        return False
    return all([user.is_active, user.account_activated, profile.resume, profile.phone_number, profile.address])
