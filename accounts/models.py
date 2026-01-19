from email.encoders import encode_noop

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ============================================
# USER MANAGER
# ============================================
class UserManager(BaseUserManager):
    "odddiy user yaratish"
    def create_user(self, email, username, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    "admin create"
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, **extra_fields)




# ============================================
# USER MODEL
# ============================================
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    Email orqali login qilish
    """

    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Ism')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Familiya')

    is_active = models.BooleanField(default=True)  # Akkaunt aktiv/bloklangan
    is_staff = models.BooleanField(default=False)  # Admin panelga kirish
    is_superuser = models.BooleanField(default=False)  # Superuser huquqlari

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Qo\'shilgan sana')

    USERNAME_FIELD = 'email'  # Login qilish uchun email ishlatiladi
    REQUIRED_FIELDS = ['username']  # Qo'shimcha majburiy maydonlar

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """To'liq ismni qaytaradi"""
        return f"{self.first_name} {self.last_name}".strip()


# ============================================
# PROFILE MODEL
# ============================================
class Profile(models.Model):
    """
    User profil ma'lumotlari
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name='Bio')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    location = models.CharField(max_length=100, blank=True, verbose_name='Manzil')
    website = models.URLField(blank=True, verbose_name='Website')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"