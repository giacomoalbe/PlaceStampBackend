from django.conf.urls import patterns, include, url
from django.contrib import admin

from autenticazione.views import LoginView, LogoutView



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PlaceStampAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('autenticazione.urls')),
    url(r'^api-auth/login/', LoginView.as_view()),
    url(r'^api-auth/logout/', LogoutView.as_view()),
    #url(r'^api-auth/', include('rest_framework.urls',
    #							namespace = 'rest_framework')),
)
