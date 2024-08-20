from blog.forms import CommentForm, EditProfileForm, PostForm
from blog.models import Category, Comment, Post
from constants import DISPLAY_ON_PAGE
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render


def get_post(get_object: bool, post_id: int = 0, filter: bool = False):
    if filter:
        return get_object_or_404(
            Post.objects.post_filter().select_related(
                'author', 'location', 'category').order_by('-pub_date'),
            pk=post_id)
    if get_object:
        return get_object_or_404(
            Post.objects.select_related(
                'author', 'location', 'category').order_by('-pub_date'),
            pk=post_id)
    else:
        return Post.objects.select_related(
            'author', 'location', 'category').order_by('-pub_date')


def paginator(request, posts):
    return Paginator(posts, DISPLAY_ON_PAGE).get_page(request.GET.get('page'))


def index(request):
    page_obj = paginator(request,
                         get_post(False).comment_count().post_filter())
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def category_posts(request, category_slug):
    category = get_object_or_404(Category
                                 .objects
                                 .category_post_filter(category_slug))
    post_list = get_post(False).filter(
        category=category).post_filter().comment_count()
    context = {'category': category, 'page_obj': paginator(request, post_list)}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if not instance.author == request.user:
        post = get_post(True, post_id, True)
    else:
        post = get_post(True, post_id)
    form = CommentForm(request.POST or None)
    comment = Comment.objects.filter(post=post_id).order_by(
        'created_at').select_related('post')
    context = {'post': post, 'form': form, 'comments': comment}
    return render(request, 'blog/detail.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    if not profile == request.user:
        posts = get_post(False).filter(
            author__username=username).post_filter().comment_count()
    else:
        posts = get_post(False).filter(
            author__username=username).comment_count()
    context = {'profile': profile, 'page_obj': paginator(request, posts)}
    return render(request, 'blog/profile.html', context)


@login_required
def create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


def edit_profile(request, username):
    instance = get_object_or_404(User, username=username)
    if instance != request.user:
        return redirect('blog:profile', username=username)
    form = EditProfileForm(request.POST or None,
                           files=request.FILES or None,
                           instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=username)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


def password_change(request):
    if request.user:
        return render(request, 'registration/password_change_form.html',)


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
    instance = get_post(True, post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


def edit_post(request, post_id):
    instance = get_post(True, post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


def edit_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id)
    if instance.author != request.user:
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
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html', {'comment': instance})
