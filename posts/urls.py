from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),

    # Post pages & actions
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('repost/<int:post_id>/', views.repost, name='repost'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),  # top-level on a post

    # Comment thread page + actions
    path('c/<int:comment_id>/', views.comment_thread, name='comment_thread'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('comment/<int:comment_id>/repost/', views.repost_comment, name='repost_comment'),
]
