from django.contrib import admin

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


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


class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category',
        'created_at',
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category', 'location',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',)
    list_editable = (
        'is_published',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
