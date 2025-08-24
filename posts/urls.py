from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),

    # Post actions
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("repost/<int:post_id>/", views.repost, name="repost"),

    # Comments
    path("comments/add/<int:post_id>/", views.add_comment, name="add_comment"),
    path("comments/reply/<int:comment_id>/", views.reply_comment, name="reply_comment"),
    path("comments/<int:comment_id>/like/", views.like_comment, name="like_comment"),
    path("comments/<int:comment_id>/repost/", views.repost_comment, name="repost_comment"),

    # NEW: dedicated thread page for a single comment (and its replies)
    path("comment/<int:comment_id>/", views.comment_detail, name="comment_detail"),
]
