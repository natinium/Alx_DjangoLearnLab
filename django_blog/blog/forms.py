from django import forms
from .models import Post, Comment
from taggit.forms import TagField, TagWidget  # Import TagWidget

class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=TagWidget(), required=False)  # Use TagWidget for tags

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']