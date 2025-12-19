from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    likes = models.ManyToManyField(
        User,
        related_name='liked_article',
        blank=True
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='Passionate entrepreneur and business strategist. Helping startups scale through data-driven decisions and smart leadership.', blank=True)

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    blog = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by "{self.user.username}" on "{self.blog.title}"'
    

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reply')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by "{self.user.username}" To "{self.comment.user.username}"'