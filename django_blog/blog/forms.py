from django import forms
from .models import Post, Comment
from taggit.forms import TagField, TagWidget

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        widget=TagWidget(attrs={'class': 'form-control'}), 
        required=False
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'})
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content here'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here'})
    )

    class Meta:
        model = Comment
        fields = ['content']
