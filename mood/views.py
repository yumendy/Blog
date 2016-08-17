from django.core.urlresolvers import reverse_lazy
from utils.mixin import AjaxableResponseMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from mood.models import Mood
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from website.mixin import FrontMixin


class MoodCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    login_url = reverse_lazy('user-login')
    model = Mood
    fields = ['title', 'content', 'mood_type', 'image']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('mood-list')

    def get_context_data(self, **kwargs):
        context = super(MoodCreateView, self).get_context_data(**kwargs)
        context['active_page'] = 'mood-add'
        return context


class MoodListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('user-login')
    model = Mood
    context_object_name = 'mood_list'

    def get_context_data(self, *args, **kwargs):
        context = super(MoodListView, self).get_context_data(**kwargs)
        context['active_page'] = 'mood-list'
        return context


class MoodUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    login_url = reverse_lazy('user-login')
    model = Mood
    context_object_name = 'mood'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('mood-list')
    fields = ['title', 'content', 'mood_type', 'image']

    def get_context_data(self, *args, **kwargs):
        context = super(MoodUpdateView, self).get_context_data(**kwargs)
        context['active_page'] = 'mood-update'
        return context


class MoodDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    login_url = reverse_lazy('user-login')
    model = Mood
    success_url = reverse_lazy('link-list')

    def post(self, request, *args, **kwargs):
        super(MoodDeleteView, self).post(request, *args, **kwargs)
        return JsonResponse({'state': 'success'})


class MoodTimeLineView(FrontMixin, ListView):
    model = Mood
    paginate_by = 20
    template_name = 'mood/mood_time_line.html'
    context_object_name = 'mood_list'
