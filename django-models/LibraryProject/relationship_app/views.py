from django.shortcuts import render, redirect
from .models import Book
from .models import Library
from .models import UserProfile
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.views.generic.detail import DetailView

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

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
    return render(request, 'relationship_app/register.html', {'form': form})

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')