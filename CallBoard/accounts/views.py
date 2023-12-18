import os
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect

from .models import OneTimeCode
from .forms import BaseSignupForm, OneTimeCodeForm

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


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

            if not OneTimeCode.objects.filter(user=user.username).exists():
                code = str(randint(100000, 999999))
                OneTimeCode.objects.create(user=user.username, code=code)
                user = User.objects.get(username=user.username)

                send_mail(
                    subject='Код активации',
                    message=f'Ваш код активации: {code}',
                    from_email=os.getenv('MAIN_EMAIL'),
                    recipient_list=[user.email]
                )

        return redirect('post_code')


class GetOneTimeCode(CreateView):

    form_class = OneTimeCodeForm
    model = OneTimeCode
    template_name = 'account/code.html'

    def form_valid(self, form):

        if 'code' in self.request.POST:
            if OneTimeCode.objects.filter(code=self.request.POST['code']).exists():
                user_list = OneTimeCode.objects.filter(code=self.request.POST['code']).values_list('user', flat=True)
                User.objects.filter(username=user_list[0]).update(is_active=True)
                OneTimeCode.objects.filter(code=self.request.POST['code'], user=user_list[0]).delete()
            else:
                return render(self.request, 'account/invalid_code.html')

        return redirect('http://127.0.0.1:8000/user_auth/login/')


class CompleteSignView(LoginRequiredMixin, TemplateView):
    template_name = 'account/complete_signup.html'


class QuitView(TemplateView):
    template_name = 'account/complete_logout.html'


class PostCodeView(TemplateView):
    template_name = 'account/code.html'
