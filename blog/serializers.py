from rest_framework import serializers
from .models import Category, Post, Comment
from accounts.serializers import UserSerializer


# ============================================
# CATEGORY SERIALIZER
# ============================================
class CategorySerializer(serializers.ModelSerializer):
    """
    Kategoriya serializer
    """
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_posts_count(self, obj):
        """Shu kategoriyada nechta post borligini qaytaradi"""
        return obj.posts.filter(status='published').count()


# ============================================
# COMMENT SERIALIZER
# ============================================
class CommentSerializer(serializers.ModelSerializer):
    """
    Kommentariya serializer
    """
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    replies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'parent', 'replies', 'replies_count',
                  'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_replies(self, obj):
        """
        Javoblarni (replies) qaytaradi
        """
        if obj.parent is None:  # Faqat asosiy commentlar uchun
            replies = obj.replies.filter(is_approved=True)
            return CommentSerializer(replies, many=True).data
        return []


# ============================================
# POST LIST SERIALIZER (Ro'yxat uchun - qisqacha)
# ============================================
class PostListSerializer(serializers.ModelSerializer):
    """
    Postlar ro'yxati uchun (qisqacha ma'lumot)
    """
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'excerpt', 'image',
                  'status', 'views_count', 'comments_count', 'created_at', 'published_at']
        read_only_fields = ['id', 'slug', 'views_count', 'created_at']


# ============================================
# POST DETAIL SERIALIZER (Batafsil)
# ============================================
class PostDetailSerializer(serializers.ModelSerializer):
    """
    Bitta postni batafsil ko'rish uchun
    """
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'content', 'excerpt',
                  'image', 'status', 'views_count', 'comments_count', 'comments',
                  'created_at', 'updated_at', 'published_at']
        read_only_fields = ['id', 'slug', 'views_count', 'created_at', 'updated_at']

    def get_comments(self, obj):
        """
        Faqat asosiy kommentariyalarni qaytaradi (parent=None)
        Replies ularning ichida
        """
        comments = obj.comments.filter(parent=None, is_approved=True).order_by('-created_at')
        return CommentSerializer(comments, many=True).data


# ============================================
# POST CREATE/UPDATE SERIALIZER
# ============================================
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Post yaratish va yangilash uchun
    """

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'excerpt', 'image', 'status', 'published_at']

    def validate_title(self, value):
        """
        Sarlavha kamida 5 ta belgi bo'lishi kerak
        """
        if len(value) < 5:
            raise serializers.ValidationError("Sarlavha kamida 5 ta belgidan iborat bo'lishi kerak!")
        return value


# ============================================
# COMMENT CREATE SERIALIZER
# ============================================
class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Kommentariya yaratish uchun
    """

    class Meta:
        model = Comment
        fields = ['post', 'content', 'parent']

    def validate_content(self, value):
        """
        Kommentariya kamida 3 ta belgi bo'lishi kerak
        """
        if len(value) < 3:
            raise serializers.ValidationError("Kommentariya kamida 3 ta belgidan iborat bo'lishi kerak!")
        return value