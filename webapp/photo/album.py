from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import AlbumForm
from webapp.models import Album, Photo


class CreateAlbumView(LoginRequiredMixin, CreateView):
    model = Album
    template_name = 'album/create.html'
    form_class = AlbumForm

    def form_valid(self, form):
        authors = self.request.user
        album = form.save(commit=False)
        album.author_album = authors
        album.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:index')


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'album/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(album=self.object, private=False)
        return context


class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/update.html'
    context_object_name = 'album'
    permission_required = 'webapp.change_album'

    def get_success_url(self):
        return reverse('webapp:view_album', kwargs={'pk': self.kwargs.get('pk')})

    def has_permission(self):
        return super().has_permission() or self.get_object().author_album == self.request.user


class AlbumDeleteView(PermissionRequiredMixin, DeleteView):
    model = Album
    template_name = 'album/delete.html'
    context_object_name = 'album'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_album'

    def has_permission(self):
        return super().has_permission() or self.get_object().author_album == self.request.user
