from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo, Album


class ListPhoto(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "photo/index.html"
    context_object_name = "photos"
    ordering = ('-created_at',)

    def get_queryset(self):
        return Photo.objects.filter(Q(private=False)).exclude(Q(album__private=True))


class PhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    context_object_name = 'photo'
    template_name = 'photo/view.html'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        authors = self.request.user
        photo = form.save(commit=False)
        photo.author = authors
        photo.save()
        return super().form_valid(form)


class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/update.html'
    context_object_name = 'photo'
    permission_required = 'webapp.change_photo'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user


class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo/delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_photo'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user
