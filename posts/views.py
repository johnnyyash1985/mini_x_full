from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
            return redirect("feed")

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
    return redirect("feed")

@login_required
def repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Post.objects.create(user=request.user, content=post.content, reposted_from=post)
    return redirect("feed")

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect("feed")

from django.http import HttpResponse

def comment_post(request, post_id):
    return HttpResponse("Comment feature coming soon!")

# --- added for post detail navigation ---
from django.shortcuts import get_object_or_404, redirect

def post_detail(request, post_id):
    from .models import Post  # local import to avoid any circulars
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/detail.html', {'post': post})

# ===== Comment actions =====
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment

@login_required
def like_comment(request, comment_id):
    c = get_object_or_404(Comment, id=comment_id)
    if request.user in c.likes.all():
        c.likes.remove(request.user)
    else:
        c.likes.add(request.user)
    return redirect("feed")

@login_required
def reply_comment(request, comment_id):
    c = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        text = (request.POST.get('content') or '').strip()
        if text:
            Comment.objects.create(
                user=request.user,
                post=c.post,
                parent=c,
                content=text[:200],
            )
    return redirect("feed")

@login_required
def repost_comment(request, comment_id):
    c = get_object_or_404(Comment, id=comment_id)
    # Create a new Post quoting the comment
    quote = f'“{c.content}” — @{c.user.username}'
    Post.objects.create(
        user=request.user,
        content=quote[:280],
        reposted_from=c.post
    )
    return redirect("feed")


@login_required
def like_comment(request, comment_id):
    c = get_object_or_404(Comment, id=comment_id)
    if request.user in c.likes.all():
        c.likes.remove(request.user)
    else:
        c.likes.add(request.user)
    next_url = request.META.get("HTTP_REFERER") or reverse("post_detail", args=[c.post_id])
    return redirect(next_url)


@login_required
def reply_comment(request, comment_id):
    c = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        text = (request.POST.get('content') or '').strip()
        if text:
            Comment.objects.create(
                user=request.user,
                post=c.post,
                parent=c,
                content=text[:200],
            )
    next_url = request.META.get("HTTP_REFERER") or reverse("post_detail", args=[c.post_id])
    return redirect(next_url)


@login_required
def repost_comment(request, comment_id):
    c = get_object_or_404(Comment, id=comment_id)
    quote = f'“{c.content}” — @{c.user.username}'
    Post.objects.create(user=request.user, content=quote[:280], reposted_from=c.post)
    next_url = request.META.get("HTTP_REFERER") or reverse("feed")
    return redirect(next_url)


@login_required
def comment_thread(request, comment_id):
    root = get_object_or_404(Comment, id=comment_id)
    return render(request, 'posts/comment_thread.html', {'root': root, 'post': root.post})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Only top-level comments; replies are rendered recursively in the partial
    top_comments = post.comments.filter(parent__isnull=True).order_by("created")
    return render(request, 'posts/detail.html', {'post': post, 'top_comments': top_comments})


@login_required
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Reply inside this thread
    if request.method == "POST":
        content = (request.POST.get("content") or "").strip()
        if content:
            Comment.objects.create(
                post=comment.post, user=request.user, content=content, parent=comment
            )
            return redirect("comment_detail", comment_id=comment.id)

    context = {
        "post": comment.post,
        "root_comment": comment,
    }
    return render(request, "posts/comment_detail.html", context)


from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        post.delete()
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("feed")
    # If someone GETs the URL, just send them back to the post
    return redirect("post_detail", post_id=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden("Not allowed")
    parent_post_id = comment.post_id
    if request.method == "POST":
        comment.delete()
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("post_detail", post_id=parent_post_id)
    # If GET, bounce to the comment’s thread
    return redirect("comment_detail", comment_id=comment_id)
from django.contrib.auth.decorators import login_required

@login_required
def reply_to_comment(request, comment_id):
    # Alias to the existing implementation
    return reply_comment(request, comment_id)
