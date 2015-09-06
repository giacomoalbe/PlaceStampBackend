from django.conf.urls import url
from autenticazione import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^upload/$', views.Upload.as_view()),
	url(r'^foto/$', views.FindPhotos.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)