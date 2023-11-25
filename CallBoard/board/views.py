import os
import random

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Announcement, Category, Respond
# from .filters import PostFilter
from .forms import AnnouncementForm
# from .tasks import send_email_post_created


class AnnouncementList(ListView):

    model = Announcement
    queryset = Announcement.objects.order_by('-pub_date')
    template_name = 'announcements.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

    # def post(self, request, *args, **kwargs):
    #
    #     if request.method == 'POST':
    #         request.session['django_timezone'] = request.POST['timezone']
    #         return redirect('posts')


class AnnouncementDetail(DetailView):

    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcement'


class AnnouncementCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = (
        'announcement.add_post'
    )

    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_add.html'
    success_url = reverse_lazy('successful')

    def form_valid(self, form):
        announcement = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        announcement.user = self.request.user
        announcement.save()
        # send_email_post_created.delay(post.id)

        return super().form_valid(form)


class AnnouncementUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = (
        'announcement.change_post'
    )

    # form_class = PostForm
    model = Announcement
    template_name = 'announcement_edit.html'
    success_url = reverse_lazy('announcements')

    def form_valid(self, form):

        announcement = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        return super().form_valid(form)


class AnnouncementDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = (
        'announcement.delete_post'
    )

    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcements')


class MainPageView(View):

    def get(self, request):

        return render(request, 'welcome.html')


class CategoryList(View):

    model = Category
    queryset = Category.objects.all()
    template_name = 'category_list.html'
    context_object_name = 'categories'


def announcements_in_category_list(request, id_ctg):

    announcements = Announcement.objects.filter(category__id=id_ctg).order_by('-pub_date')
    cur_ctg = Category.objects.get(id=id_ctg)
    context = {
        'announcements': announcements,
        'cur_ctg': cur_ctg,
    }

    return render(request, 'announcements_in_category_list.html', context=context)


def login_view(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # login(request, user)
        # OneTimeCode.objects.create(code=random.choice('12345'), user=user)
        return render(request, 'welcome.html')

    else:
        pass


def login_with_code_view(request):

    username = request.POST['username']
    code = request.POST['code']
    # if OneTimeCode.objects.filter(code=code, user__username=username).exists():
    #   login(request, user)
    # else:
    #   pass


@login_required
def successful_page_view(request):

    return render(request, 'successful.html')
