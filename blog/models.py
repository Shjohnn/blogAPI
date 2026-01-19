from django.db import models
from django.conf import settings
from django.utils.text import slugify


# ============================================
# CATEGORY MODEL
# ============================================
class Category(models.Model):
    """
    Blog kategoriyalari (Technology, Health, Travel va h.k.)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Kategoriya nomi')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Slug avtomatik yaratish"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ============================================
# POST MODEL
# ============================================
class Post(models.Model):
    """
    Blog postlari
    """

    # Status choices
    STATUS_CHOICES = (
        ('draft', 'Draft'),  # Qoralama
        ('published', 'Published'),  # Nashr qilingan
    )

    # Asosiy ma'lumotlar
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Muallif'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Kategoriya'
    )

    # Kontent
    content = models.TextField(verbose_name='Matn')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Qisqacha')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Rasm')

    # Status va sanalar
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='O\'zgartirilgan')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Nashr qilingan')

    # Statistika
    views_count = models.PositiveIntegerField(default=0, verbose_name='Ko\'rishlar soni')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        """Slug avtomatik yaratish"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def comments_count(self):
        """Kommentariyalar soni"""
        return self.comments.count()


# ============================================
# COMMENT MODEL
# ============================================
class Comment(models.Model):
    """
    Post kommentariyalari
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Muallif'
    )
    content = models.TextField(verbose_name='Kommentariya')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Javob'
    )

    # Status
    is_approved = models.BooleanField(default=True, verbose_name='Tasdiqlangan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='O\'zgartirilgan')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.post.title[:30]}"

    @property
    def replies_count(self):
        """Javoblar soni"""
        return self.replies.count()
