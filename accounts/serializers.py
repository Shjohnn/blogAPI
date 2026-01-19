from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

# ============================================
# LOGIN SERIALIZER
# ============================================
class LoginSerializer(serializers.Serializer):
    """
    Login uchun serializer
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})




class UserSerializer(serializers.ModelSerializer):
    """
    User malumotini serializer orqali json format ga otkazamz
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id","created_at","updated_at")


# PROFILE SERIALIZER
# ============================================
class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile modelini JSON ga aylantirish
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar', 'phone', 'location', 'website', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Yangi user yaratsh uchun serializer
    """
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        """
        parollar birhilligini tekshrsh
        """
        if attrs['password'] != attrs['password']:
            raise serializers.ValidationError('Password and password must match')
        return attrs

    def create(self, validated_data):
        """
        User yaratsh
        """
        validated_data.pop('password2') #password2 ni ohiramz
        user =User.objects.create_user(**validated_data)

        Profile.objects.create(user=user)

        return user


#User update serializer
class UserUpdateSerializer(serializers.Serializer):
     class Meta:
         model = User
         fields =['first_name','last_name']

#Profile update serializer
class ProfileUpdateSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = '__all__'