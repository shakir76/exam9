from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class Photo(models.Model):
    avatar = models.ImageField(upload_to='avatars', verbose_name="Фото")
    signature = models.CharField(max_length=50, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authors",
                               verbose_name="Автор")
    album = models.ForeignKey('webapp.Album', on_delete=models.CASCADE, related_name="albums",
                              null=True, blank=True, verbose_name="Альбом")
    private = models.BooleanField(default=False, verbose_name='Приватный')
    favorites = models.ManyToManyField(get_user_model(), related_name="favorites_photo")

    def __str__(self):
        return f"{self.id}. {self.author}: {self.signature}"

    # def get_absolute_url(self):
    #     return reverse('webapp:index')

    class Meta:
        db_table = "Photo"
        verbose_name = "Фото"
        verbose_name_plural = "Фото"


class Album(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Описание")
    author_album = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authors_album",
                                     verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    private = models.BooleanField(default=False, verbose_name='Приватный')
    favorites = models.ManyToManyField(get_user_model(), related_name="favorites_album")

    def __str__(self):
        return f"{self.id}. {self.name}: {self.author_album}"

    class Meta:
        db_table = "Album"
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
