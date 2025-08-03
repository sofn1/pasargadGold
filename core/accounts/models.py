from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# ======================
# USER MANAGER
# ======================
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "superadmin")

        if extra_fields.get("role") != "superadmin":
            raise ValueError("Superuser must have role of 'superadmin'")
        return self.create_user(phone_number, password, **extra_fields)


# ======================
# USER MODEL
# ======================
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('writer', 'Writer'),
        ('admin', 'Admin'),
        ('superadmin', 'Superadmin'),
    )

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone_number} ({self.role})"


# ======================
# COMMON USER FIELDS
# ======================
class ProfileBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True


# ======================
# CUSTOMER PROFILE
# ======================
class Customer(ProfileBase):
    address = models.TextField()
    location = models.CharField(max_length=256, blank=True, null=True)


# ======================
# SELLER PROFILE
# ======================
class Seller(ProfileBase):
    email = models.EmailField()
    about_us = models.TextField()
    profile_image = models.ImageField(upload_to="sellers/")
    address = models.TextField()
    location = models.CharField(max_length=256, blank=True, null=True)
    business_name = models.CharField(max_length=128)
    business_code = models.CharField(max_length=64)


# ======================
# WRITER PROFILE
# ======================
class Writer(ProfileBase):
    email = models.EmailField()
    about_me = models.TextField()
    profile_image = models.ImageField(upload_to="writers/")


class WriterPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='writer_permission')
    can_write_blogs = models.BooleanField(default=False)
    can_write_news = models.BooleanField(default=False)


# ======================
# ADMIN PROFILE
# ======================
class AdminPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_superadmin = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)


class AdminInviteToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

