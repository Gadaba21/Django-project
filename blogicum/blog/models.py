from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models

from constants import MAX_LENGTH

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def post_filter(self):
        now = datetime.now()
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now,)


class CategoryQuerySet(models.QuerySet):
    def category_post_filter(self, category_slug):
        return self.filter(
            slug=category_slug,
            is_published=True)


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Location(PublishedModel):
    name = models.CharField(
        'Название места',
        max_length=MAX_LENGTH
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=MAX_LENGTH
    )
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.')

    objects = CategoryQuerySet.as_manager()

    class Meta(PublishedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=MAX_LENGTH,
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    objects = PostQuerySet.as_manager()

    class Meta(PublishedModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:profile', args=[self.author.username])