from django import forms

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(author_album=user)

    class Meta:
        model = Photo
        fields = ['avatar', 'signature', 'album', 'private']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description', 'private']