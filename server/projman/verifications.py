#    This file is part of Lithium-Projman.
#
#    Lithium-Projman is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Lithium-Projman is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lithium-Projman.  If not, see <http://www.gnu.org/licenses/>.


import re
from .models import *


def get_or_none(model, *args, **kwargs):
	try:
		return model.objects.get(*args, **kwargs)
	except model.DoesNotExist:
		return None



EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]*$')

def userIsLogged(user):
    #user.is_anonymous() returns True if there's a cookie that's not associated with an existing account
    #user.is_active() should always return True, returns false if an admin deactivated the account
    return (not user.is_anonymous() and user.is_active)


def emailIsValid(email):
    return bool(EMAIL_REGEX.match(email))


def usernameExists(username):
    return User.objects.filter(username = username).exists()


def userParticipatesProject(user, project):
    puser = get_or_none(ProjmanUser, user = user)
    return Participation.objects.filter(user = puser, project = project).exists()


def usernameIsValid(username):
    return (bool(username) and bool(USERNAME_REGEX.match(username)))


def userIsAuthor(user, entity):
    puser = get_or_none(ProjmanUser, user = user)
    return entity.author == puser
