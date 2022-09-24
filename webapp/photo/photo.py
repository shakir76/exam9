from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from webapp.models import Photo


class ListPhoto(ListView):
    model = Photo
    template_name = "photo/index.html"
    context_object_name = "photos"
    ordering = ('-created_at',)


class PhotoView(DetailView):
    model = Photo
    context_object_name = 'photo'
    template_name = 'photo/view.html'
