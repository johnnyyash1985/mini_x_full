from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Comment
from social.models import Follow

@login_required
def feed(request):
    # People I follow + me
    following_ids = list(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    ) + [request.user.id]
    posts = Post.objects.filter(user_id__in=following_ids).order_by('-created')

    # Composer
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Post.objects.create(user=request.user, content=content)
            return redirect("post_detail", post_id=post_id)

    # Suggestions: not me, not already followed
    exclude_ids = set(following_ids)
    suggest_users = User.objects.exclude(id__in=exclude_ids).order_by('-date_joined')[:5]

    return render(request, 'posts/feed.html', {'posts': posts, 'suggest_users': suggest_users})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("post_detail", post_id=post_id)

@login_required
def repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Post.objects.create(user=request.user, content=post.content, reposted_from=post)
    return redirect("post_detail", post_id=post_id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect("post_detail", post_id=post_id)

from django.http import HttpResponse

def comment_post(request, post_id):
    return HttpResponse("Comment feature coming soon!")

# --- added for post detail navigation ---
from django.shortcuts import get_object_or_404, redirect

def post_detail(request, post_id):
    from .models import Post  # local import to avoid any circulars
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/detail.html', {'post': post})
