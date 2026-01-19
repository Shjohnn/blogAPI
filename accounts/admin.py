from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


# ============================================
# USER ADMIN
# ============================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin panelda User modelini sozlash
    """

    # List page - ro'yxatda qaysi ustunlar ko'rinadi
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']

    # Filter - o'ng tomonda filtrlash
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'date_joined']

    # Search - qidiruv
    search_fields = ['email', 'username', 'first_name', 'last_name']

    # Detail page - user ma'lumotlarini ko'rish/tahrirlash
    fieldsets = (
        ('Login Ma\'lumotlari', {
            'fields': ('email', 'username', 'password')
        }),
        ('Shaxsiy Ma\'lumotlar', {
            'fields': ('first_name', 'last_name')
        }),
        ('Ruxsatlar', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Muhim Sanalar', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Yangi user qo'shishda qaysi fieldlar ko'rinadi
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    # Default tartiblash
    ordering = ['-date_joined']

    # Faqat o'qish uchun fieldlar
    readonly_fields = ['date_joined', 'last_login']


# ============================================
# PROFILE ADMIN
# ============================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin panelda Profile modelini sozlash
    """

    # List page
    list_display = ['user', 'phone', 'location', 'created_at']

    # Filter
    list_filter = ['created_at', 'updated_at']

    # Search
    search_fields = ['user__email', 'user__username', 'phone', 'location']

    # Detail page
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Ma\'lumotlar', {
            'fields': ('bio', 'avatar', 'phone', 'location', 'website')
        }),
        ('Sanalar', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # Faqat o'qish
    readonly_fields = ['created_at', 'updated_at']

    # Default tartiblash
    ordering = ['-created_at']