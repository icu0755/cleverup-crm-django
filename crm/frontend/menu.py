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