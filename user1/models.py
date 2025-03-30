from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#-----------------------------------------------------------------------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    """Manager for CustomUser model"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Automatically hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
#-----------------------------------------------------------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model extending Django authentication system"""

    email = models.EmailField(unique=True)  # Unique identifier
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True, default="profile_pics/default_profile.png")
    date_of_birth = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)  # Required for admin login

    objects = CustomUserManager()

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email