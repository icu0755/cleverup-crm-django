import random
import string
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from frontend.forms import LoginForm, RegForm


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
