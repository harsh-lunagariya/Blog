from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list_view, name='home'),

    path('create/blog/', views.blog_create_view, name='createBlog'),
    path('edit/<str:slug>/', views.blog_edit_view, name='editBlog'),
    path('delete/<str:slug>/', views.blog_delete_view, name='deleteBlog'),
    
    path('blog/<str:slug>/', views.article, name='blog'),
    path('blog/like/<str:slug>/', views.like_post, name='blog_like'),

    path('c/<str:slug>/',views.comment_view, name='comment'),
    path('c/d/<str:slug>/<int:comment_id>/',views.comment_delete_view, name='commentDelete'),
    path('r/<str:slug>/<int:comment_id>/',views.comment_reply_view, name='reply'),
    path('r/d/<str:slug>/<int:reply_id>/',views.reply_delete_view, name='replyDelete'),
]
