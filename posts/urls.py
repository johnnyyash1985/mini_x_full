from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/repost/', views.repost, name='repost'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),

    # NEW: delete post
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # Comments
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/repost/', views.repost_comment, name='repost_comment'),

    # NEW: delete comment/reply
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
