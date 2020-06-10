from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.forms import User 

def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 11)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(request, "index.html", {"page": page, "paginator": paginator})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    paginator = Paginator(post_list, 11)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(request, "group.html", {"group": group, "page": page, "paginator": paginator})

def new_post(request):        
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')
            
        return render(request, 'new_post.html', {'form': form})

    form = PostForm()
    return render(request, 'new_post.html', {'form': form})

def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(
            request,
            "profile.html",
            {
            "author": author,"post": post_list, "page": page, "paginator": paginator
          })
 
def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id) 
    author = get_object_or_404(User, username=username)
    return render(request, 'post.html', {"profile": author, "post": post})
# или лучже пейджинатор и обрботку формы вынести отдельными функциями?
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id) 
    author = get_object_or_404(User, username=username)
    if request.user != author:
        return redirect(
                'post',
                username=post.author.username,
                post_id=post_id
            )
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(
                    'post',
                    username=request.user.username,
                    post_id=post_id
                    )
    form = PostForm()
    return render(request, 'new_post.html', {'form': form,'post': post})