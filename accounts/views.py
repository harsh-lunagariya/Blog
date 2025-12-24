from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .forms import RegisterForm, LoginForm, EditProfileForm
from django.views.decorators.cache import never_cache
from .models import Profile
from myapp.models import Article

# Create your views here.

User = get_user_model()

@require_http_methods(["GET","POST"])
def register_view(request):
    # if user already logged in then it can not access this view
    if request.user.is_authenticated:     
        return redirect('home')

    # error_msg = None
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
            login(request,user)
            return render(request, 'accounts/register.html', {'form':form})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

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