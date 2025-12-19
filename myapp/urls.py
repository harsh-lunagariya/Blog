from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',views.logout_view, name='logout'),

    path('create/blog/', views.blog_create_view, name='createBlog'),
    path('edit/<int:article_id>/', views.blog_edit_view, name='editBlog'),
    path('delete/<int:article_id>/', views.blog_delete_view, name='deleteBlog'),
    path('edit/<str:username>', views.edit_profile , name='editProfile'),
    
    path('blog/<int:article_id>/', views.article, name='blog'),
    path('blog/like/<int:article_id>/', views.like_post, name='blog_like'),
    path('u/<str:username>/', views.user_profile, name='profile'),

    path('c/<int:article_id>/',views.comment_view, name='comment'),
    path('c/d/<int:article_id>/<int:comment_id>/',views.comment_delete_view, name='commentDelete'),
    path('r/<int:article_id>/<int:comment_id>/',views.comment_reply_view, name='reply'),
    path('r/d/<int:article_id>/<int:reply_id>/',views.reply_delete_view, name='replyDelete'),
]
