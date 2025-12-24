from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',views.logout_view, name='logout'),

    path('u/<str:username>/', views.user_profile, name='profile'),
    path('edit/<str:username>/', views.edit_profile , name='editProfile'),
]
