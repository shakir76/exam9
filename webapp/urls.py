from django.urls import path

# from webapp.photo.photo import ListProduct
#
from webapp.photo import ListPhoto, PhotoView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, CreateAlbumView, \
    AlbumDetailView, AlbumUpdateView, AlbumDeleteView, GetUrls, PhotoGetURLS, AddFavorites, AddFavoritesAlbum

app_name = 'webapp'
#
urlpatterns = [
    path('', ListPhoto.as_view(), name="index"),
    path('photo/create/', PhotoCreateView.as_view(), name="create_photo"),
    path('photo/<int:pk>/', PhotoView.as_view(), name="view_photo"),
    path('photo/<int:pk>/update', PhotoUpdateView.as_view(), name="update_photo"),
    path('photo/<int:pk>/delete', PhotoDeleteView.as_view(), name="delete_photo"),
    path('album/add', CreateAlbumView.as_view(), name="add_album"),
    path('album/<int:pk>/view/', AlbumDetailView.as_view(), name="view_album"),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name="delete_album"),
    path('album/<int:pk>/update', AlbumUpdateView.as_view(), name="update_album"),
    path('gets/links/<int:pk>/', GetUrls.as_view(), name="get_urls"),
    path('gets/links/<uuid>', PhotoGetURLS.as_view(), name='photo_urls'),
    path('add/favorites/<int:pk>/', AddFavorites.as_view(), name="add_favorites"),
    path('add/favorites/album/<int:pk>/', AddFavoritesAlbum.as_view(), name="add_favorites_album"),

]
