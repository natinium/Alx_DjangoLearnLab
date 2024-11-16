from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Book, Library
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.core.exceptions import PermissionDenied

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
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
    try:
        return user.is_authenticated and user.userprofile.role == 'Admin'
    except AttributeError:
        return False

def is_librarian(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Librarian'
    except AttributeError:
        return False

def is_member(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Member'
    except AttributeError:
        return False

@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    """
    View for admin users only
    """
    context = {
        'role': 'Admin',
        'permissions': ['Manage Users', 'Manage Roles', 'View All Content']
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    """
    View for librarian users only
    """
    context = {
        'role': 'Librarian',
        'permissions': ['Manage Books', 'View Members', 'Issue Books']
    }
    return render(request, 'librarian_dashboard.html', context)

@user_passes_test(is_member, login_url='login')
def member_view(request):
    """
    View for member users only
    """
    context = {
        'role': 'Member',
        'permissions': ['View Books', 'Borrow Books', 'View Profile']
    }
    return render(request, 'member_dashboard.html', context)