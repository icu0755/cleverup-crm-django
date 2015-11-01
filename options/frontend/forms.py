from django import forms
from django.core import validators

__author__ = 'vi'


class TrimmedCharFormField(forms.CharField):
    def clean(self, value):
        if value:
            value = value.strip()
        return super(TrimmedCharFormField, self).clean(value)


class NewUserForm(forms.Form):
    """
    New user form
    """
    email = TrimmedCharFormField(
        label='Email',
        widget=forms.EmailInput,
        required=True,
        validators=[validators.validate_email],
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True,
    )


class LoginForm(forms.Form):
    email = TrimmedCharFormField(
        label='Email',
        max_length=100,
        validators=[validators.RegexValidator(r'[a-z0-9-@\.]+\.[a-z]{2,}', 'Invalid Email')],
        required=True,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True,
    )


class RegForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        validators=[validators.validate_email],
        required=True
    )



