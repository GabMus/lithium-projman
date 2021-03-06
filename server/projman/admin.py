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


from django.contrib import admin
from .models import *

admin.site.register(ProjmanUser)
admin.site.register(Project)
admin.site.register(To_do)
admin.site.register(Comment_todo)
admin.site.register(Designation)
admin.site.register(Note)
admin.site.register(Participation)
admin.site.register(Projcode)
# Register your models here.
