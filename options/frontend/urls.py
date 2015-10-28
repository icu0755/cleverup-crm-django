from django.conf import settings
from django.conf.urls.static import static
from frontend import views

__author__ = 'vi'

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
                  url(r'^/?$', views.home, name='home'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
