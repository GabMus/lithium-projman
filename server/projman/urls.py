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


from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

	url(r'^$', views.index, name = 'index'),
	url(r'^signup/?', views.signup, name = 'signup'),
	url(r'^signin/?', views.signin, name = 'signin'),
	url(r'^submitsignin/?', views.submitsignin, name = 'submitsignin'),
	url(r'^submitsignup/?', views.submitsignup, name = 'submitsignup'),
	url(r'^submitinvitesignup/?', views.submitinvitesignup, name = 'submitinvitesignup'),
	url(r'^signout/?', views.signout, name = 'signout'),

	url(r'^submitnewproj/?', views.submitnewproj, name = 'submitnewproj'),

	url(r'^project/(?P<projid>[0-9]+)/?$', views.projview, name = 'projview'),
	url(r'^project/(?P<projid>[0-9]+)/notes?$', views.notesview, name = 'notesview'),

	url(r'^submitnewtodo/?', views.submitnewtodo, name = 'submitnewtodo'),
	url(r'^submitnewnote/?', views.submitnewnote, name = 'submitnewnote'),

	url(r'^toggleTodoDone/(?P<todoid>[0-9]+)/?$', views.toggletododone, name = 'toggleTodoDone'),

	url(r'^deletetodo/(?P<todoid>[0-9]+)/?$', views.deletetodo, name = 'deletetodo'),
	url(r'^deletenote/(?P<noteid>[0-9]+)/?$', views.deletenote, name = 'deletenote'),

	url(r'^todo/(?P<todoid>[0-9]+)/?$', views.todoview, name = 'todoview'),
	url(r'^note/(?P<noteid>[0-9]+)/?$', views.notecommentsview, name = 'notecommentsview'),
	url(r'^submittodocomment/(?P<todoid>[0-9]+)/?$', views.submittodocomment, name = 'submittodocomment'),
	url(r'^deletetodocomment/(?P<commentid>[0-9]+)/?$', views.deletetodocomment, name = 'deletetodocomment'),

	url(r'^editnote/?', views.editnote, name = 'editnote'),
	url(r'^submitnotecomment/(?P<noteid>[0-9]+)/?$', views.submitnotecomment, name = 'submitnotecomment'),
	url(r'^deletenotecomment/(?P<commentid>[0-9]+)/?$', views.deletenotecomment, name = 'deletenotecomment'),

	url(r'^edittodo/?', views.edittodo, name = 'edittodo'),

	url(r'^uploadpic/?', views.userpicupload, name = 'uploadpic'),

	url(r'^sendinvite/?$', views.sendinvite, name = 'sendinvite'),
	url(r'^getinvite/(?P<email>[^@]+@[^@]+\.[^@]+)/(?P<projcode>.+)/?$', views.getinvite, name = 'getinvite'),
	url(r'^deleteproject/?$', views.deleteproject, name = 'deleteproject'),
	url(r'^mytasks/?$', views.mytasksview, name = 'mytasks'),
	url(r'^leaveproject/(?P<projid>[0-9]+)/?$', views.leaveproject, name = 'leaveproject'),

	url(r'^kickuser/(?P<projid>[0-9]+)/(?P<username>[a-zA-Z0-9_]+)/?$', views.kickuser, name = 'kickuser'),
	url(r'^deleteuser/?$', views.deleteuser, name = 'deleteuser')

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
