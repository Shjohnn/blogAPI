from django.contrib import admin
from .models import Category, Post, Comment


# ============================================
# CATEGORY ADMIN
# ============================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Kategoriyalarni boshqarish
    """
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}  # Slug avtomatik to'ldiriladi
    ordering = ['name']


# ============================================
# COMMENT INLINE (Post ichida ko'rsatish)
# ============================================
class CommentInline(admin.TabularInline):
    """
    Post tahrirlashda kommentariyalarni ko'rsatish
    """
    model = Comment
    extra = 0  # Bo'sh formalar soni
    fields = ['author', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']


# ============================================
# POST ADMIN
# ============================================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Postlarni boshqarish
    """
    list_display = ['title', 'author', 'category', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'  # Sana bo'yicha navigatsiya
    ordering = ['-created_at']

    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Kontent', {
            'fields': ('excerpt', 'content', 'image')
        }),
        ('Status va Sanalar', {
            'fields': ('status', 'published_at')
        }),
        ('Statistika', {
            'fields': ('views_count',),
            'classes': ('collapse',)  # Yig'ilgan holda ko'rsatish
        }),
    )

    readonly_fields = ['views_count']
    inlines = [CommentInline]  # Kommentariyalarni ko'rsatish


# ============================================
# COMMENT ADMIN
# ============================================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Kommentariyalarni boshqarish
    """
    list_display = ['author', 'post', 'content_preview', 'parent', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author__username', 'content', 'post__title']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Comment Ma\'lumotlari', {
            'fields': ('post', 'author', 'content', 'parent')
        }),
        ('Status', {
            'fields': ('is_approved',)
        }),
    )

    def content_preview(self, obj):
        """Content'ning qisqartilgan ko'rinishi"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Kommentariya'