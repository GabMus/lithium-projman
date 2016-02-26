from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^signup/?', views.signup, name='signup'),
	url(r'^signin/?', views.signin, name='signin'),
	url(r'^submitsignin/?', views.submitsignin, name='submitsignin'),
	url(r'^submitsignup/?', views.submitsignup, name='submitsignup'),
	url(r'^signout/?', views.signout, name='signout'),

	url(r'^submitnewproj/?', views.submitnewproj, name='submitnewproj'),
	url(r'^updateavatar/?', views.updateavatar, name='updateavatar'),

	url(r'^project/(?P<projid>[0-9]+)/?$', views.projview, name='projview'),
	url(r'^submitnewtodo/?', views.submitnewtodo, name='submitnewtodo'),
	url(r'^toggleTodoDone/(?P<todoid>[0-9]+)/?$', views.toggletododone, name='toggleTodoDone'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #+ static(settings.MEDIA_INCOMPLETE_URL, document_root=settings.MEDIA_ROOT)
