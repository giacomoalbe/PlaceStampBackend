from django.conf.urls import url
from autenticazione import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^utenti/$', views.UserList.as_view()),
	url(r'^utenti/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	url(r'^utenti/nuovo/$', views.NewUser.as_view()),
	url(r'^post/$', views.PostList.as_view()),
	url(r'^post/(?P<id>[0-9]+)/$', views.PostUser.as_view()),
	url(r'^post/new/$', views.NewPost.as_view()),
	url(r'^owners/$', views.OwnerList.as_view()),
	url(r'^cars/$', views.CarsList.as_view()),
	url(r'^cars/(?P<pk>[0-9]+)/$', views.CarDetail.as_view()),
	url(r'^upload/$', views.Upload.as_view()),
	url(r'^foto/$', views.show_photos)
]

urlpatterns = format_suffix_patterns(urlpatterns)