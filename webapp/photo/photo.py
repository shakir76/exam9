from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo, Album


class ListPhoto(ListView):
    model = Photo
    template_name = "photo/index.html"
    context_object_name = "photos"
    ordering = ('-created_at',)

    def get_queryset(self):
        return Photo.objects.filter(Q(private=False) | Q(album__private=False))


class PhotoView(DetailView):
    model = Photo
    context_object_name = 'photo'
    template_name = 'photo/view.html'


class PhotoCreateView(CreateView):
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


class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/update.html'
    context_object_name = 'photo'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photo/delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('webapp:index')
