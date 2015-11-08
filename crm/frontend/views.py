import random
import string
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from frontend.forms import LoginForm, RegForm, CustomerGroupForm, CustomerForm, GroupAttendanceSelectForm, \
    GroupAttendanceForm, UserCreateForm, UserEditForm
from frontend.models import CustomerGroup, Customer, GroupAttendance


@login_required(login_url=settings.LOGIN_URL)
def home(request):
    return render(request, 'home.html')


def login(request):
    """
    shows login form and authenticates a user

    to create a user log in into shell
    from django.contrib.auth.models import User
    User.objects.create_user('es@infopunks.com', 'es@infopunks.com', 'password')

    :param request:
    :return:
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        redirect_url = request.GET.get('next', '/')

        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                username = User.objects.get(email=email).username
                user = auth.authenticate(username=username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect(redirect_url)
                else:
                    messages.error(request, _('your account is suspended'))
            else:
                messages.error(request, _('invalid login or password'))
    else:
        form = LoginForm()
        reg_email = request.session.get('reg_email', None)
        if reg_email is not None:
            form.fields['email'].initial = reg_email

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    auth.logout(request)
    return redirect('frontend:login')


def registration(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in
                          range(settings.DEFAULT_PASSWORD_LENGTH))

            user = User.objects.create_user(email, email, password=pwd)
            user.save()

            sign_in_url = reverse('frontend:login')

            body = """
            Hi,

            login: %s
            password: %s

            you can sign in at %s

            best regards,
            your robot
            """ % (email, pwd, request.build_absolute_uri(sign_in_url))

            html_message = """
            Hi,

            login: %s
            password: %s

            you can sign in <a href="%s">here</a>

            best regards,
            your robot
            """ % (email, pwd, request.build_absolute_uri(sign_in_url))

            request.session['reg_email'] = email

            send_mail('registration', body, settings.EMAIL_FROM, [email], html_message=html_message)
            messages.info(request,
                          _('registration succeed, the password is sent to the %(email)s') % {'email': email})

            user = auth.authenticate(username=email, password=pwd)
            auth.login(request, user)

            return redirect('/')
    else:
        form = RegForm()

    context = {
        'form': form
    }
    return render(request, 'registration.html', context)


@login_required(login_url=settings.LOGIN_URL)
def customers_list(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, _('Customer %s %s created') % (instance.firstname, instance.lastname))
            return redirect(reverse('frontend:customers-list'))
    else:
        form = CustomerForm()
    customers = Customer.objects.all()
    context = {'form': form, 'customers': customers}
    return render(request, 'customers_list.html', context)


@login_required(login_url=settings.LOGIN_URL)
def customers_edit(request, customer_id):
    try:
        instance = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, _('Customer %s does not exists') % customer_id)
        return redirect('frontend:customers-list')

    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            messages.success(request, _('Customer saved'))
            return redirect('frontend:customers-list')
    else:
        form = CustomerForm(instance=instance)

    return render(request, 'customers_edit.html', {'form': form, 'customer': instance})


@login_required(login_url=settings.LOGIN_URL)
def groups_list(request):
    if request.method == 'POST':
        form = CustomerGroupForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, _('Group %s created') % instance.name)
            return redirect(reverse('frontend:groups-list'))
    else:
        form = CustomerGroupForm()
    groups = CustomerGroup.objects.all()
    context = {'form': form, 'groups': groups}
    return render(request, 'groups_list.html', context)


@login_required(login_url=settings.LOGIN_URL)
def groups_edit(request, group_id):
    try:
        instance = CustomerGroup.objects.get(pk=group_id)
    except CustomerGroup.DoesNotExist:
        messages.error(request, _('Group %s does not exists') % group_id)
        return redirect('frontend:groups-list')

    if request.method == 'POST':
        form = CustomerGroupForm(data=request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            messages.success(request, _('Group saved'))
            return redirect('frontend:groups-list')
    else:
        form = CustomerGroupForm(instance=instance)

    return render(request, 'groups_edit.html', {'form': form, 'group': instance})


def groups_attendance(request, group_id):
    try:
        instance = CustomerGroup.objects.get(pk=group_id)
    except CustomerGroup.DoesNotExist:
        messages.error(request, _('Group %s does not exists') % group_id)
        return redirect('frontend:groups-list')

    initial = {'attendance_time': timezone.now()}
    if request.method == 'POST':
        form = GroupAttendanceSelectForm(request.POST, initial=initial)
        if form.is_valid():
            dt = form.cleaned_data['attendance_time']
            return redirect(reverse('frontend:groups-attendance-edit', kwargs={'group_id': instance.id, 'dt': dt}))
    else:
        form = GroupAttendanceSelectForm(initial=initial)
    attendance = GroupAttendance.objects.filter(group=instance).values('attendance_time').order_by('attendance_time')\
        .distinct('attendance_time')
    context = {'form': form, 'attendance': attendance, 'group': instance}
    return render(request, 'groups_attendance.html', context)


@transaction.atomic
def groups_attendance_edit(request, group_id, dt):
    try:
        instance = CustomerGroup.objects.get(pk=group_id)
    except CustomerGroup.DoesNotExist:
        messages.error(request, _('Group %s does not exists') % group_id)
        return redirect('frontend:groups-list')

    dt = timezone.datetime.strptime(dt, '%Y-%m-%d')
    initial = instance.get_attendance(dt)
    if request.method == 'POST':
        form = GroupAttendanceForm(request.POST, group=instance, initial=initial)
        if form.is_valid():
            for customer_field, value in form.cleaned_data.iteritems():
                none, customer_id = customer_field.split('_')
                customer_id = int(customer_id)
                customer = Customer.objects.get(id=customer_id)
                if value and not initial[customer_field]:
                    GroupAttendance.objects.create(group=instance, customer=customer, attendance_time=dt)
                if not value and initial[customer_field]:
                    GroupAttendance.objects.filter(group=instance, customer=customer, attendance_time=dt).delete()

            messages.success(request, _('Attendance saved'))
            return redirect(reverse('frontend:groups-attendance', kwargs={'group_id': instance.id}))
    else:
        form = GroupAttendanceForm(group=instance, initial=initial)
    context = {'form': form, 'group': instance, 'dt': dt.strftime('%Y-%m-%d')}
    return render(request, 'groups_attendance_edit.html', context)


@login_required(login_url=settings.LOGIN_URL)
def users_list(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            instance = User.objects.create_user(email, email, password)
            instance.is_staff = True
            instance.save()
            messages.success(request, _('User %s created') % instance.username)
            return redirect(reverse('frontend:users-list'))
    else:
        form = UserCreateForm()
    users = User.objects.filter(is_superuser=False, is_active=True)
    context = {'users': users, 'form': form}
    return render(request, 'users_list.html', context)


@login_required(login_url=settings.LOGIN_URL)
def users_edit(request, user_id):
    try:
        instance = User.objects.filter(is_superuser=False, is_active=True).get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, _('User %s does not exists') % user_id)
        return redirect('frontend:users-list')

    initial = {
        'email': instance.email,
    }
    if request.method == 'POST':
        form = UserEditForm(request.POST, initial=initial)
        if form.is_valid():
            instance.email = instance.username = form.cleaned_data['email']
            if 'password' in form.changed_data:
                password = form.cleaned_data['password']
                instance.set_password(password)
            instance.save()
            messages.success(request, _('User saved'))
            return redirect('frontend:users-list')
    else:
        form = UserEditForm(initial=initial)

    return render(request, 'users_edit.html', {'form': form, 'user': instance})


@login_required(login_url=settings.LOGIN_URL)
def users_remove(request, user_id):
    try:
        instance = User.objects.get(pk=user_id)
        instance.is_active = False
        instance.save()
    except User.DoesNotExist:
        messages.error(request, _('User %s does not exists') % user_id)
    messages.success(request, _('User %s removed') % user_id)
    return redirect('frontend:users-list')