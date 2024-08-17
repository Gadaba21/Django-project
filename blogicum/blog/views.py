from blog.forms import EditProfileForm, CreatePost
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from blog.models import Category, Post
from constants import DISPLAY_ON_MAIN_PAGE




def index(request):
    posts = (Post
             .objects
             .post_filter()[:DISPLAY_ON_MAIN_PAGE]
             )
    return render(request, "blog/index.html", {"page_obj": posts})


def category_posts(request, category_slug):
    category = get_object_or_404(Category
                                 .objects
                                 .category_post_filter(category_slug))
    post_list = Post.objects.post_filter().filter(category=category)
    context = {"category": category, "page_obj": post_list}
    return render(request, "blog/category.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.post_filter(),
        pk=post_id
    )
    return render(request, "blog/detail.html", {"post": post})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__username=username)
    context = {"profile": profile, "page_obj": posts}
    return render(request, "blog/profile.html", context)


def create(request):
    form = CreatePost(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, "blog/user.html", context)

def edit_profile(request, username):
    instance = get_object_or_404(User, username=username)
    form = EditProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=username)
    context = {'form': form}
    return render(request, "blog/user.html", context)


def password_change(request):
    return render(request, "registration/password_change_form.html",)