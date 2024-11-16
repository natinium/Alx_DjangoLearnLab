from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = role
            user_profile.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Welcome, Admin!")

@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Welcome, Librarian!")

@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Welcome, Member!")