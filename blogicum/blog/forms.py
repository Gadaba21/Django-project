from django.contrib.auth.models import User
from django import forms
from blog.models import Post



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('is_published',
                   'created_at'
                   )
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }
