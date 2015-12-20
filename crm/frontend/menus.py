__author__ = 'vi'

from menu import Menu, MenuItem
from django.core.urlresolvers import reverse

"""
documentation https://django-simple-menu.readthedocs.org/en/latest/
"""


def is_authenticated():
    return lambda request: request.user.is_authenticated()


def is_anonymous():
    return lambda request: request.user.is_anonymous()


def is_superuser():
    return lambda request: request.user.is_superuser


def is_staff():
    return lambda request: request.user.is_staff

Menu.add_item("main", MenuItem("Customers",
                               reverse("frontend:customers-list"),
                               weight=10,
                               check=is_authenticated()))
Menu.add_item("main", MenuItem("Groups",
                               reverse("frontend:groups-list"),
                               weight=20,
                               check=is_authenticated()))
Menu.add_item("main", MenuItem("Users",
                               reverse("frontend:users-list"),
                               weight=30,
                               check=is_superuser()))
Menu.add_item("main", MenuItem("Payments",
                               reverse("frontend:payments-list"),
                               weight=40,
                               check=is_superuser()))
