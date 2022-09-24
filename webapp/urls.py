from django.urls import path

# from webapp.photo.photo import ListProduct
#
from webapp.photo import ListPhoto, PhotoView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView

app_name = 'webapp'
#
urlpatterns = [
    path('', ListPhoto.as_view(), name="index"),
    path('photo/create/', PhotoCreateView.as_view(), name="create_photo"),
    path('photo/<int:pk>/', PhotoView.as_view(), name="view_photo"),
    path('photo/<int:pk>/update', PhotoUpdateView.as_view(), name="update_photo"),
    path('photo/<int:pk>/delete', PhotoDeleteView.as_view(), name="delete_photo"),
    # path('product/<int:pk>/add/review', AddReview.as_view(), name="add_review"),
    # path('product/<int:pk>/update/review', UpdateReview.as_view(), name="update_review"),
    # path('product/<int:pk>/delete/review', DeleteReview.as_view(), name="delete_review"),
    # path('review/list', ListNotModerReView.as_view(), name="index_review"),

]
