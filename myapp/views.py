from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .forms import BlogForm, CommentForm, CommentReplyForm
from .models import Article, ArticleSlugHistory, Comment, CommentReply
from django.http import JsonResponse
from django.db.models import Prefetch
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.

User = get_user_model()

@require_GET
def blog_list_view(request):
    articles = Article.objects.all()
    users = User.objects.all()
    placeholder_users = []
    for user in users:
        placeholder_users.append({'username':user.username, 'fullname': f'{user.first_name} {user.last_name}'})
    return render(request, 'web/home.html',{'articles':articles,'placeholder_users': placeholder_users})

@never_cache
@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def blog_create_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'

    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, "Your blog has been posted successfully.")
            return redirect('home')
        else:
            messages.error(request, "Failed to post the blog. Please try again.")
    else:
        form = BlogForm()
    return render(request, 'web/blogForm.html',{'form':form,'next':next_url})

@require_GET
def article(request,slug):
    try:
        article = get_object_or_404(Article, slug=slug)
    except:
        oldslug_obj = get_object_or_404(ArticleSlugHistory, old_slug=slug)
        article = oldslug_obj.article
        
    date = article.created_at.date()
    comments = Comment.objects.filter(blog=article).prefetch_related(
        Prefetch('comment_reply', queryset=CommentReply.objects.all())
    )
    return render(request, 'user/blogPage.html',{'article':article,'date':date, 'comments':comments})

@never_cache
@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def blog_edit_view(request,slug):
    
    article = get_object_or_404(Article, slug=slug)
    
    if article.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Your blog has been updated successfully.")
            return redirect('profile', username = request.user.username)
        else:
            messages.error(request, "Failed to update the blog. Please try again.")
    else:
        form = BlogForm(instance=article)
    
    return render(request, 'web/blogEditForm.html', {'form':form,'article':article})

@never_cache
@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def blog_delete_view(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if article.user != request.user:
        return redirect('home')
    
    if request.method == "POST":
        article.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('profile', username = request.user.username)
    return redirect('blog', slug=slug)

@login_required(login_url='login')
def like_post(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.user in article.likes.all():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked':liked,
        'total_likes':article.total_likes()
    })

@never_cache
@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def comment_view(request,slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = article
            comment.save()
            return redirect('blog',slug)
        else:
            print("Error")
    return redirect('blog',slug)

@never_cache
@login_required(login_url='login')
@require_POST
def comment_delete_view(request,slug,comment_id):
    comment = Comment.objects.get(id = comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('blog', slug)

@never_cache
@login_required(login_url='login')
@require_POST
def comment_reply_view(request,slug,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
    return redirect('blog',slug)

@never_cache
@login_required(login_url='login')
@require_POST
def reply_delete_view(request, slug, reply_id):
    reply = CommentReply.objects.get(id = reply_id)
    if request.user == reply.user:
        reply.delete()
    return redirect('blog', slug)
