from django import forms
from django.contrib.auth import get_user_model
from .models import Article, Comment, CommentReply

User = get_user_model()

class BlogForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your title here'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your content...'}),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text']