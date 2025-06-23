from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.forms import AuthenticationForm

#1 Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("event:home")
    else:
        form = AuthenticationForm()
    
    return render(request, "user1/login.html", {"form": form})

# ---------------------------------------------------------------------------------------------------------------------------
#2 Sign up
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect("login")  # Redirect to homepage or dashboard
        else:
            print(form.errors)  # Debug: show form validation errors
    else:
        form = CustomUserCreationForm()
    
    return render(request, "user1/signup.html", {"form": form})

# ---------------------------------------------------------------------------------------------------------------------------
#14 Update profile
@login_required
def update_profile(request):
    """View to update user profile with password change option"""
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)

            # Get passwords from form
            current_password = form.cleaned_data.get("current_password")
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if current_password and new_password:
                # If the current password is incorrect
                if not request.user.check_password(current_password):
                    messages.error(request, "❌ Current password is incorrect!")
                    return redirect("update_profile")

                # If new password and confirm password do not match
                if new_password != confirm_password:
                    messages.error(request, "❌ New password and confirm password do not match!")
                    return redirect("update_profile")

                # Update password
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep user logged in

            user.save()
            return redirect("event:profile")  # Redirect to profile page
        else:
            messages.error(request, "Please check old password or your new password and confirm password are not same.")

    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, "user1/update_profile.html", {"form": form})

# ---------------------------------------------------------------------------------------------------------------------------
#19 Logout
def logout_view(request):
    logout(request)
    return redirect("login")

# ---------------------------------------------------------------------------------------------------------------------------
