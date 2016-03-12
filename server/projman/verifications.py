import re
from .models import *


EMAIL_REGEX=re.compile(r'[^@]+@[^@]+\.[^@]+')

def userIsLogged(user):
    #user.is_anonymous() returns True if there's a cookie that's not associated with an existing account
    #user.is_active() should always return True, returns false if an admin deactivated the account
    return (not user.is_anonymous() and user.is_active())

def emailIsValid(email):
    return EMAIL_REGEX.match(email)

def usernameExists(username):
    return User.filter(username=username).exists()

def userParticipatesProject(user, project):
    puser=ProjmanUser(user=user)
    return Participation.filter(user=puser, project=project).exists()
