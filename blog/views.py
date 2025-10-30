'''from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()  # sabhi posts la raha hai
    return render(request, 'post_list.html', {'posts': posts})
'''
from django.shortcuts import render

# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})
