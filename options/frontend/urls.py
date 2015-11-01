from django.conf import settings
from django.conf.urls.static import static
from frontend import views
from django.conf.urls import url

__author__ = 'vi'


urlpatterns = [
                  url(r'^/?$', views.home, name='home'),
                  url(r'^login$', views.login, name='login'),
                  url(r'^logout$', views.logout, name='logout'),
                  url(r'^registration$', views.registration, name='registration'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
