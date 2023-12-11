from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Announcement, Category, Respond
from .forms import AnnouncementForm, RespondForm
from .filters import RespondFilter
# from .tasks import send_email_post_created
# send_email_post_created.delay(post.id)


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


class AnnouncementDetail(DetailView):

    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcement'


class AnnouncementCreate(LoginRequiredMixin, CreateView):

    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_add.html'
    success_url = reverse_lazy('successful_announcement')

    def form_valid(self, form):
        announcement = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        announcement.user = self.request.user
        announcement.save()

        return super().form_valid(form)


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):

    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'
    success_url = reverse_lazy('announcements')

    def form_valid(self, form):

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        return super().form_valid(form)


class AnnouncementDelete(LoginRequiredMixin, DeleteView):

    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcements')


class CategoryList(ListView):

    model = Category
    queryset = Category.objects.all()
    template_name = 'category_list.html'
    context_object_name = 'categories'


class RespondList(ListView):

    model = Respond
    template_name = 'responds.html'
    context_object_name = 'responds'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context

    def get_queryset(self):
        anns_list = Announcement.objects.filter(user=self.request.user).values_list('id', flat=True)
        responds = Respond.objects.filter(
            announcement__id__in=anns_list, denied__exact=False).order_by('-respond_date')
        queryset = responds
        self.filterset = RespondFilter(self.request.GET, queryset)

        return self.filterset.qs


class RespondDetail(DetailView):

    model = Respond
    template_name = 'respond.html'
    context_object_name = 'respond'


class RespondCreate(LoginRequiredMixin, CreateView):

    form_class = RespondForm
    model = Respond
    template_name = 'respond_add.html'
    success_url = reverse_lazy('successful_respond')

    def form_valid(self, form):
        respond = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        respond.user = self.request.user
        respond.announcement_id = self.kwargs['pk']
        respond.save()

        return super().form_valid(form)


class MainPageView(View):

    def get(self, request):

        return render(request, 'welcome.html')


def announcements_own_list(request):

    announcements = Announcement.objects.filter(user=request.user).order_by('-pub_date')
    context = {
        'announcements': announcements,
    }

    return render(request, 'announcements.html', context=context)


def announcements_in_category_list(request, id_ctg):

    announcements = Announcement.objects.filter(category__id=id_ctg).order_by('-pub_date')
    cur_ctg = Category.objects.get(id=id_ctg)
    context = {
        'announcements': announcements,
        'cur_ctg': cur_ctg,
    }

    return render(request, 'announcements_in_category_list.html', context=context)


@login_required
def successful_announcement_view(request):

    return render(request, 'successful_announcement.html')


@login_required
def successful_respond_view(request):

    return render(request, 'successful_respond.html')


@login_required
def accept_respond(request, id_res):

    Respond.objects.filter(id=id_res).update(confirmed=True)

    # отправить письмо автору отклика

    return redirect(f'http://127.0.0.1:8000/announcements/responds_list/')


@login_required
def denied_respond(request, id_res):

    Respond.objects.filter(id=id_res).update(denied=True)

    return redirect(f'http://127.0.0.1:8000/announcements/responds_list/')
