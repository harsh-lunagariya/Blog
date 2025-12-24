from django.db import models
from django.conf import settings

# Create your models here.

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True,max_length=220, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog')
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_article',
        blank=True
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    
class ArticleSlugHistory(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="slug_history"
    )
    old_slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.old_slug
   

class Comment(models.Model):
    blog = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by "{self.user.username}" on "{self.blog.title}"'
    

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reply')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by "{self.user.username}" To "{self.comment.user.username}"'