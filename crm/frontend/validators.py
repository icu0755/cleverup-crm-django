from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

__author__ = 'Pixel'


def validate_user_not_exists(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(_('User already exists'), code='already_exists')
