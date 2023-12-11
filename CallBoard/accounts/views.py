import os
from random import randint

from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect

from .models import OneTimeCode
from .forms import BaseSignupForm


class BaseRegisterView(CreateView):

    form_class = BaseSignupForm
    model = User
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = BaseSignupForm()

        return context

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

        return redirect('code_confirm', request.POST['username'])


class GetOneTimeCode(CreateView):

    template_name = 'account/code.html'

    def get_context_data(self, **kwargs):

        user_name = self.kwargs.get('user')

        if not OneTimeCode.objects.filter(user=user_name).exists():
            code = str(randint(100000, 999999))
            OneTimeCode.objects.create(user=user_name, code=code)
            user = User.objects.get(username=user_name)

            send_mail(
                    subject='Код активации',
                    message=f'Ваш код активации: {code}',
                    from_email=os.getenv('MAIN_EMAIL'),
                    recipient_list=[user.email]
            )

    def post(self, request, *args, **kwargs):

        if 'code' in request.POST:
            user = request.path.split('/')[-1]
            if OneTimeCode.objects.filter(code=request.POST['code'], user=user).exists():
                User.objects.filter(username=user).update(is_active=True)
                OneTimeCode.objects.filter(code=request.POST['code'], user=user).delete()
            else:
                return render(self.request, 'account/invalid_code.html')

        return redirect('login')


class CompleteSignView(LoginRequiredMixin, TemplateView):
    template_name = 'account/complete_signup.html'


class QuitView(TemplateView):
    template_name = 'account/complete_logout.html'


def login_view(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # login(request, user)
        # OneTimeCode.objects.create(code=random.choice('12345'), user=user)
        return render(request, '')

    else:
        pass


def login_with_code_view(request):

    username = request.POST['username']
    code = request.POST['code']
    # if OneTimeCode.objects.filter(code=code, user__username=username).exists():
    #   login(request, user)
    # else:
    #   pass
