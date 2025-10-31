'''from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')'''
        


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post


# --- Blog Post Form ---
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')  # Post model में जो fields हैं वही लिखो


# --- Signup Form ---
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']





















