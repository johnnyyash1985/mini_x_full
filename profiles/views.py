from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from social.models import Follow

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    is_following = False
    if request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    return render(request, 'profiles/profile.html', {
        'profile_user': user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'profiles/edit_profile.html', {'profile': profile})
