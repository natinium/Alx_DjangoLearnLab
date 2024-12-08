from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("profile")
        else:
            messages.error(request, "Registration failed.")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("profile")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

@login_required
def profile_view(request):
    return render(request, "blog/profile.html", {"user": request.user})

@login_required
def edit_profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email", request.user.email)
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    return render(request, "blog/edit_profile.html", {"user": request.user})

