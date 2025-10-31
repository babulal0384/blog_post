from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, SignUpForm


# -------------------- BLOG VIEWS --------------------

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# -------------------- AUTH (SIGNUP, LOGIN, LOGOUT) --------------------

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')  # Signup के बाद Blog पर redirect
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  # Login के बाद Blog पर redirect
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid username or password'})
    return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Logout के बाद Login पेज पर redirect



from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # अगर user इस post का author नहीं है तो उसे मना करो
    if post.author != request.user:
        return HttpResponseForbidden("❌ You cannot edit this post. It doesn’t belong to you.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 🧠 केवल वही user delete कर सकता है जिसने post बनाई हो
    if post.author != request.user:
        return HttpResponseForbidden("❌ आप इस पोस्ट को हटा नहीं सकते। यह आपकी नहीं है।")

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

