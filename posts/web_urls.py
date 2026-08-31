from django.urls import path
from .views import home, post_detail, create_post, edit_post

urlpatterns = [
    path('', home, name='home'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create-post/', create_post, name='create_post'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),
]