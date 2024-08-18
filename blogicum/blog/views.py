from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import CommentForm, EditProfileForm, PostForm
from blog.models import Category, Comment, Post


def paginator(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    posts = (Post
             .objects
             .post_filter()
             ).order_by('-pub_date',)
    page_obj = paginator(request, posts)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def category_posts(request, category_slug):
    category = get_object_or_404(Category
                                 .objects
                                 .category_post_filter(category_slug))
    post_list = Post.objects.post_filter().filter(
        category=category).order_by('-pub_date',)
    page_obj = paginator(request, post_list)
    context = {"category": category, "page_obj": page_obj}
    return render(request, "blog/category.html", context)


def post_detail(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if not instance.author == request.user:
        post = get_object_or_404(
            Post.objects.post_filter(),
            pk=post_id
        )
    else:
        post = get_object_or_404(
            Post.objects,
            pk=post_id
        )
    form = CommentForm(request.POST or None)
    comment = Comment.objects.filter(post=post_id).order_by('created_at')
    context = {"post": post, "form": form, "comments": comment}
    return render(request, "blog/detail.html", context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    if not profile == request.user:
        posts = Post.objects.post_filter().filter(
            author__username=username).order_by('-pub_date',)
    else:
        posts = Post.objects.filter(
            author__username=username).order_by('-pub_date',)
    page_obj = paginator(request, posts)
    context = {"profile": profile, "page_obj": page_obj}
    return render(request, "blog/profile.html", context)


@login_required
def create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, "blog/user.html", context)


def edit_profile(request, username):
    instance = get_object_or_404(User, username=username)
    if not request.user.is_authenticated or instance != request.user:
        return redirect('blog:profile', username=username)
    form = EditProfileForm(request.POST or None,
                           files=request.FILES or None,
                           instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=username)
    context = {'form': form}
    return render(request, "blog/user.html", context)


def password_change(request):
    if request.user:
        return render(request, "registration/password_change_form.html",)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.post = get_object_or_404(Post, pk=post_id)
        post.save()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/post_detail.html', {'form': form})


def delete_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    if not request.user.is_authenticated or instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


def edit_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated or instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form}
    return render(request, "blog/user.html", context)


def edit_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id)
    if not request.user.is_authenticated or instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = CommentForm(request.POST or None, instance=instance)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.post = get_object_or_404(Post, pk=post_id)
        post.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form, 'comment': instance}
    return render(request, 'blog/comment.html', context)


def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, id=comment_id)
    if not request.user.is_authenticated or instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html', {'comment': instance})
