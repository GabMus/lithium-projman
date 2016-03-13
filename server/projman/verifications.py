import re
from .models import *


EMAIL_REGEX=re.compile(r'[^@]+@[^@]+\.[^@]+')
USERNAME_REGEX=re.compile(r'^[a-zA-Z0-9_]*$')

def userIsLogged(user):
    #user.is_anonymous() returns True if there's a cookie that's not associated with an existing account
    #user.is_active() should always return True, returns false if an admin deactivated the account
    return (not user.is_anonymous() and user.is_active)

def emailIsValid(email):
    return bool(EMAIL_REGEX.match(email))

def usernameExists(username):
    return User.filter(username=username).exists()

def userParticipatesProject(user, project):
    puser=ProjmanUser.objects.get(user=user)
    return Participation.objects.filter(user=puser, project=project).exists()

def usernameIsValid(username):
    return (bool(username) and bool(USERNAME_REGEX.match(username)))
