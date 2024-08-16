from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<str:username>/', views.profile,
         name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile,
         name='edit_profile'),
    path('profile/<str:username>/password_change/', views.password_change,
         name='password_change'),
    path('profile/<str:username>/password/', views.password_change,
         name='password'),
    path('posts/create_post/', views.PostCreateView.as_view(),
         name='create_post'),
]

