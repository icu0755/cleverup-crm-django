from django.conf import settings
from django.conf.urls.static import static
from frontend import views
from django.conf.urls import url

__author__ = 'vi'


urlpatterns = [
                  url(r'^/?$', views.home, name='home'),
                  url(r'^customers$', views.customers_list, name='customers-list'),
                  url(r'^customers/(?P<customer_id>\d+)/edit$', views.customers_edit, name='customers-edit'),
                  url(r'^groups$', views.groups_list, name='groups-list'),
                  url(r'^groups/(?P<group_id>\d+)/edit$', views.groups_edit, name='groups-edit'),
                  url(r'^groups/(?P<group_id>\d+)/customer_add$', views.groups_customer_add,
                      name='groups-customer-add'),
                  url(r'^groups/(?P<group_id>\d+)/attendance$', views.groups_attendance, name='groups-attendance'),
                  url(r'^groups/(?P<group_id>\d+)/attendance_report$', views.groups_attendance_report,
                      name='groups-attendance-report'),
                  url(r'^groups/(?P<group_id>\d+)/attendance/(?P<dt>\d{4}\-\d{2}\-\d{2})$',
                      views.groups_attendance_edit, name='groups-attendance-edit'),
                  url(r'^login$', views.login, name='login'),
                  url(r'^logout$', views.logout, name='logout'),
                  url(r'^users/?$', views.users_list, name='users-list'),
                  url(r'^users/(?P<user_id>\d+)/edit$', views.users_edit, name='users-edit'),
                  url(r'^users/(?P<user_id>\d+)/remove$', views.users_remove, name='users-remove'),
                  # url(r'^registration$', views.registration, name='registration'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
