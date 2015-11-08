from django import forms
from django.core import validators
from django.core.validators import validate_email
from django.forms.utils import ErrorList
from django.utils.translation import ugettext as _
from frontend import models
from frontend.validators import validate_user_not_exists

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


class CustomerGroupForm(forms.ModelForm):
    class Meta:
        model = models.CustomerGroup
        fields = ['name']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['firstname', 'lastname', 'group']


class GroupAttendanceForm(forms.Form):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, group=None):
        super(GroupAttendanceForm, self).__init__(data, files, auto_id, prefix, initial,
                                                  error_class, label_suffix, empty_permitted)
        self.group = group
        self.add_customers()

    def add_customers(self):
        for customer in self.group.customers.all():
            field_name = 'customer_%s' % customer.id
            field = forms.BooleanField(label='%s %s' % (customer.firstname, customer.lastname), required=False)
            self.fields[field_name] = field


class GroupAttendanceSelectForm(forms.Form):
    attendance_time = forms.DateField(label=_('Date'), widget=forms.DateInput(attrs={'class': 'cu-datepicker'}))


class UserCreateForm(forms.Form):
    email = TrimmedCharFormField(
        label=_('Email'),
        widget=forms.EmailInput,
        required=True,
        validators=[validate_email, validate_user_not_exists],
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True,
    )


class UserEditForm(forms.Form):
    email = TrimmedCharFormField(
        label=_('Email'),
        widget=forms.EmailInput,
        required=True,
        validators=[validate_email],
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=False,
    )

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, group=None):
        super(UserEditForm, self).__init__(data, files, auto_id, prefix, initial,
                                                  error_class, label_suffix, empty_permitted)
        self.init_fields()

    def init_fields(self):
        self.init_email_validators()

    def init_email_validators(self):
        if 'email' in self.changed_data:
            self.fields['email'].validators.append(validate_user_not_exists)


