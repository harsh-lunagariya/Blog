from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .form import RegisterForm, LoginForm, BlogForm, EditProfileForm, CommentForm, CommentReplyForm
from .models import Article,Profile, Comment, CommentReply
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.db.models import Prefetch

# Create your views here.

@require_GET
def blog_list_view(request):
    articles = Article.objects.all()
    users = User.objects.all()
    placeholder_users = []
    for user in users:
        placeholder_users.append({'username':user.username, 'fullname': f'{user.first_name} {user.last_name}'})
    return render(request, 'web/home.html',{'articles':articles,'placeholder_users': placeholder_users})

@require_http_methods(["GET","POST"])
def register_view(request):
    # if user already logged in then it can not access this view
    if request.user.is_authenticated:     
        return redirect('home')

    error_msg = None
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
            login(request,user)
            return redirect('home')
        else:
            error_msg= 'Username already taken!'
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form, 'error':error_msg})

@never_cache
@require_http_methods(["GET","POST"])
def login_view(request):
    if request.user.is_authenticated:     
        return redirect('home')

    error_msg = None
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(next_url)
            else:
                error_msg = "Invalid Credentials!"
        else:
            error_msg = "Please fill in the form correctly!"
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form,'error':error_msg,'next':next_url})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home') 
    
    
@login_required
@require_http_methods(["GET","POST"])
def blog_create_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'

    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'web/blogForm.html',{'form':form,'next':next_url})

@login_required
@require_http_methods(["GET","POST"])
def blog_edit_view(request,article_id):
    article = get_object_or_404(Article, article_id=article_id)
    
    if article.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('profile', username = request.user.username)
    else:
        form = BlogForm(instance=article)
    
    return render(request, 'web/blogEditForm.html', {'form':form,'article':article})


@login_required
@require_http_methods(["GET","POST"])
def blog_delete_view(request, article_id):
    article = get_object_or_404(Article,pk=article_id)

    if article.user != request.user:
        return redirect('home')
    
    if request.method == "POST":
        article.delete()
        return redirect('profile', username = request.user.username)
    return render(f'blog/{article_id}')
    

@require_GET
def article(request,article_id):
    article = Article.objects.get(article_id=article_id)
    date = article.created_at.date()
    comments = Comment.objects.filter(blog=article).prefetch_related(
        Prefetch('comment_reply', queryset=CommentReply.objects.all())
    )
    return render(request, 'user/blogPage.html',{'article':article,'date':date, 'comments':comments})

@login_required
def like_post(request, article_id):
    article_obj = Article.objects.get(article_id = article_id)
    if request.user in article_obj.likes.all():
        article_obj.likes.remove(request.user)
        liked = False
    else:
        article_obj.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked':liked,
        'total_like':article_obj.total_likes()
    })


@login_required
@require_http_methods(["GET","POST"])
def comment_view(request,article_id):
    article = Article.objects.get(article_id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = article
            comment.save()
            return redirect('blog',article_id)
        else:
            print("Error")
    return redirect('blog',article_id)

@require_POST
def comment_delete_view(request,article_id,comment_id):
    comment = Comment.objects.get(id = comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('blog', article_id)

@require_POST
def comment_reply_view(request,article_id,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
    return redirect('blog',article_id)
    
@require_POST
def reply_delete_view(request, article_id, reply_id):
    reply = CommentReply.objects.get(id = reply_id)
    if request.user == reply.user:
        reply.delete()
    return redirect('blog', article_id)


@require_GET
def user_profile(request,username):
    user = User.objects.get(username= username)
    articles = Article.objects.filter(user=user)
    flag = articles.exists()
    profile = Profile.objects.get(user=user)
    bio=profile.bio
    return render(request, 'user/profile.html',{'userprofile':user,"articles":articles,'flag':flag,'bio':bio})

@require_http_methods(["GET","POST"])
def edit_profile(request,username):
    user = User.objects.get(username= username)
    profile = get_object_or_404(Profile,user=user)
    if profile.user != request.user:
        return redirect('home')
    
    if request.method =='POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile',username=username)
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'user/editProfile.html', {'form':form})