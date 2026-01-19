from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from unicodedata import category

from .models import *
from .serializers import *


# category view
class CategoryListView(generics.ListCreateAPIView):
    """
    GET /api/categories/ - Barcha kategoriyalar
    POST /api/categories/ - Yangi kategoriya yaratish (faqat admin)
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET /api/categories/<id>/ - Kategoriya detali
        PUT/PATCH /api/categories/<id>/ - Kategoriyani yangilash (admin)
        DELETE /api/categories/<id>/ - O'chirish (admin)
        """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# post veiw
class PostListView(generics.ListAPIView):
    """
        GET /api/posts/ - Barcha postlar (faqat published)
        Search: ?search=django
        Filter: ?category=1&author=2
        """
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'content', 'author__username')
    ordering_fields = ('-created_at', 'views_count')

    def get_queryset(self):
        """
            Faqat published postlarni ko'rsatish
            Filter qo'shish
        """
        queryset = Post.objects.filter(status='published').select_related('author', 'category')
        #category boyicha filter
        category=self.request.query_params.get('category', None)
        if category:
            queryset=queryset.filter(category_id=category)

        #author boyicha filter
        author=self.request.query_params.get('author', None)
        if author:
            queryset=queryset.filter(author_id=author)

        return queryset

class PostDetailView(APIView):
    """
        GET /api/posts/<slug>/ - Post detali
        """
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status='published')

        #korishlar sonini hisoblash
        post.views += 1
        post.save(update_fields=['views'])
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class PostCreateView(generics.CreateAPIView):
    """
    POST /api/posts/create/ - Yangi post yaratish (login kerak)
    """
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Author'ni avtomatik qo'shish"""
        serializer.save(author=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        """Faqat o'z postlarini tahrirlash"""
        # Swagger uchun
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        """Faqat o'z postlarini o'chirish"""
        # Swagger uchun
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)


class MyPostsView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Swagger uchun
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user).select_related('category')

# ============================================
# COMMENT VIEWS
# ============================================
class CommentListView(generics.ListAPIView):
    """
    GET /api/comments/ - Barcha kommentariyalar
    GET /api/comments/?post=1 - Bitta post commentlari
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_approved=True).select_related('author', 'post')

        # Post bo'yicha filter
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id, parent=None)  # Faqat asosiy commentlar

        return queryset


class CommentCreateView(generics.CreateAPIView):
    """
    POST /api/comments/create/ - Yangi comment yaratish (login kerak)
    Body: {"post": 1, "content": "Zo'r post!", "parent": null}
    """
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Author'ni avtomatik qo'shish"""
        serializer.save(author=self.request.user)


class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Faqat o'z commentlarini tahrirlash"""
        # Swagger uchun
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        return Comment.objects.filter(author=self.request.user)


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Faqat o'z commentlarini o'chirish"""
        # Swagger uchun
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        return Comment.objects.filter(author=self.request.user)