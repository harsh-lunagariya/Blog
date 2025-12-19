from django import forms
from django.contrib.auth.models import User
from .models import Article,Profile, Comment, CommentReply

class BlogForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your title here'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your content...'}),
        }
        

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','password','password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError("Password do not match!")
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text']