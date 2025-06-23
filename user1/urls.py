from django.urls import path
from . import views

# localhost:8000/

urlpatterns = [
    path("", views.login_view, name="login"),  #1 Custom login view

    path("signup/", views.signup_view, name="signup"),  #2 User registration

    path("profile/update/", views.update_profile, name="update_profile"),  #14 User profile update

    path("logout/", views.logout_view, name="logout"),  #18 Logs out user and redirects to login
]