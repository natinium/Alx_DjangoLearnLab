from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})