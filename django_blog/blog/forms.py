from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget  # Import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content here'}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Add tags separated by commas'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here'}),
        }
