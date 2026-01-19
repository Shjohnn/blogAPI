from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import *
from .models import Profile


# royhatdan otish
class RegisterView(generics.CreateAPIView):
    """
    yangi user yaratish     /api/auth/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # token yaratish
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            },
            'message': 'User muvaffaqiiyatli yaratildi'
        }, status=status.HTTP_201_CREATED)


# login view
class LoginView(generics.GenericAPIView):
    """
    Login qilish
    POST /api/auth/login/
    Body: {"email": "user@gmail.com", "password": "pass123"}
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # User tekshirish
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Email yoki parol noto\'g\'ri!'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Token yaratish
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Login muvaffaqiyatli!'
            }
        )
# logout view

class LogoutView(APIView):
    """
    logout qlish (tokenni ochirish) /api/auth/logout/
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()  # tokenni qora royxatga qoshish

            return Response({
                'message': 'Muvaffaqiiyatli logout'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': "Xatolik yuz berdi"},
                status.HTTP_400_BAD_REQUEST
            )


# profile view (oz profilini korish va tahrirlash)

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/profile/ - O'z profilini ko'rish
    PUT/PATCH /api/auth/profile/ - Profilni tahrirlash
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Joriy user'ning profili"""
        return self.request.user.profile

    def get_serializer_class(self):
        """GET uchun ProfileSerializer, PUT/PATCH uchun ProfileUpdateSerializer"""
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileUpdateSerializer
        return ProfileSerializer


# ============================================
# USER DETAIL VIEW (Boshqa userlarni ko'rish)
# ============================================
class UserDetailView(generics.RetrieveAPIView):
    """
    GET /api/users/<id>/ - Boshqa user'ning profilini ko'rish
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    from django.contrib.auth import get_user_model
    queryset = get_user_model().objects.all()