from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('repost/<int:post_id>/', views.repost, name='repost'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
