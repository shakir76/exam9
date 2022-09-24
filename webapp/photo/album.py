from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import AlbumForm
from webapp.models import Album, Photo


class CreateAlbumView(CreateView):
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


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(album=self.object, private=False)
        return context


class AlbumUpdateView(UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/update.html'
    context_object_name = 'album'

    def get_success_url(self):
        return reverse('webapp:view_album', kwargs={'pk': self.kwargs.get('pk')})


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'album/delete.html'
    context_object_name = 'album'
    success_url = reverse_lazy('webapp:index')


