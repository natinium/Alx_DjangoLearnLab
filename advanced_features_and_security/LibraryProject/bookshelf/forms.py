from django import forms
from .models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']  # Include other fields as necessary

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)