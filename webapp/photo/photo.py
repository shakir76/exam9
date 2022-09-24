from uuid import uuid4

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo, Album, NewUrls


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


class GetUrls(PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=self.kwargs.get('pk'))
        links = uuid4().hex
        NewUrls.objects.create(photo=photo, link_url=links)
        return redirect('webapp:view_photo', pk=photo.pk)

    def has_permission(self):
        photo = get_object_or_404(Photo, pk=self.kwargs.get('pk'))
        return self.request.user == photo.author


class PhotoGetURLS(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('uuid')
        photo = Photo.objects.get(urls_photo__link_url=pk)
        context = {'photo': photo}
        return render(request, 'photo/view.html', context=context)


class AddFavorites(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=self.kwargs.get('pk'))
        users = self.request.user
        if users in photo.favorites.all():
            photo.favorites.remove(users)
        else:
            photo.favorites.add(users)
        photo_favorites = users in photo.favorites.all()
        return JsonResponse({'user': photo_favorites})
