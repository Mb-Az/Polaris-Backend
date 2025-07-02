from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, user_type="regular", **extra_fields):
        if user_type == "regular" and not email:
            raise ValueError("Regular users must have an email address")

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, user_type=user_type, **extra_fields)

        if user_type == "regular":
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, user_type="regular", **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("regular", "Regular User"),
        ("device", "Mobile Device"),
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="regular")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Devices can have email blank, so handle accordingly
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email if self.email else f"Device User {self.id}"
