from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'title',
        'is_published',
        'description',
        'slug',)
    list_editable = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category',
        'created_at',
        'comments_count',
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category', 'location',)

    @admin.display(description="Количество комментариев")
    def comments_count(self, obj):
        return obj.comments.count()


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',)
    list_editable = (
        'is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'post',)


admin.site.unregister(Group)
