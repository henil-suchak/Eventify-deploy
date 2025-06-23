from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

#-----------------------------------------------------------------------------------------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    """Custom Sign-up Form with Profile Picture Support"""

    class Meta:
        model = CustomUser
        fields = ["name", "email", "phone_number", "profile_picture", "password1", "password2"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500",
                "placeholder": "Full Name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500",
                "placeholder": "Email Address"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500",
                "placeholder": "Phone Number"
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500 pr-10",
                "placeholder": "Create Password",
                "autocomplete": "new-password",
                "style": "color: black !important;",
                "id": "password1"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500 pr-10",
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
                "style": "color: black !important;",
                "id": "password2"
            }),
        }

#-----------------------------------------------------------------------------------------------------------------------------------
CustomUser = get_user_model()

class CustomUserUpdateForm(forms.ModelForm):
    """Form to update user profile with an option to change password"""

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Enter Current Password"
        }),
        required=False,
        label="Current Password",
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Enter New Password"
        }),
        required=False,
        label="New Password",
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Confirm New Password"
        }),
        required=False,
        label="Confirm New Password",
    )

    class Meta:
        model = CustomUser
        fields = ["name", "email", "phone_number", "date_of_birth", "profile_picture"]

        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'
            }),
            "email": forms.EmailInput(attrs={
                "readonly": "readonly",
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'
            }),
            "phone_number": forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'
            }),
            "date_of_birth": forms.DateInput(attrs={
                "type": "date",
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError("You must enter your current password to change the password.")
            if not self.instance.check_password(current_password):
                raise forms.ValidationError("Current password is incorrect.")
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
    
#-----------------------------------------------------------------------------------------------------------------------------------
