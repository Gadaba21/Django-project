from django import forms
from django.contrib.auth.models import User

from blog.models import Comment, Post
from constants import COMMENT_WINDOW_SIZE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': COMMENT_WINDOW_SIZE})
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('is_published',
                   'created_at',
                   'author'
                   )
        widgets = {
            'pub_date': forms.DateInput(
                attrs={'type': 'date', 'format': 'YYYY-MM-DD'}
            )
        }
