from django.contrib import admin

# Register your models here.
from webapp.models import Photo, Album


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author']
    list_display_links = ['author']
    list_filter = ['author']
    search_fields = ['author']
    fields = ['author', 'signature', 'private', 'avatar', 'created_at', 'album']
    readonly_fields = ['created_at']


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['name', 'description', 'author', 'created_at']
    readonly_fields = ['created_at']


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
