from django.urls import include, path

from . import views

app_name = 'blog'

post_endpoints = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create, name='create_post'),
    path('<post_id>/edit/', views.edit_post, name='edit_post'),
    path('<post_id>/delete/', views.delete_post, name='delete_post'),
    path('<post_id>/comment/', views.add_comment, name='add_comment'),
    path('<post_id>/delete_comment/<comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('<post_id>/edit_comment/<comment_id>/',
         views.edit_comment, name='edit_comment'),
]

profile_endpoints = [
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/edit/',
         views.edit_profile, name='edit_profile'),
    path('<str:username>/password_change/',
         views.password_change, name='password_change'),
    path('<str:username>/password/',
         views.password_change, name='password'),
]

category_endpoints = [
    path('<slug:category_slug>/',
         views.category_posts, name='category_posts'),
]


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', include(post_endpoints)),
    path('profile/', include(profile_endpoints)),
    path('category/', include(category_endpoints)),
]
