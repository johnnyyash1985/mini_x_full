from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    reposted_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='reposts')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    # NEW: likes for comments
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    # NEW: threaded replies
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'@{self.user.username} on Post {self.post_id}: {self.content[:30]}'
