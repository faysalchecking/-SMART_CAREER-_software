from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    """Serialize user information"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize user profile with user details"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'phone', 'address', 'is_active']

class LoginSerializer(serializers.Serializer):
    """Validate login credentials"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')

        # Authenticate with username and password
        from django.contrib.auth import authenticate
        authenticated_user = authenticate(username=user.username, password=password)

        if not authenticated_user:
            raise serializers.ValidationError('Invalid email or password.')

        data['user'] = authenticated_user
        return data

class LoginResponseSerializer(serializers.Serializer):
    """Response serializer for login"""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserSerializer()

class MeSerializer(serializers.Serializer):
    """Response serializer for current user"""
    user = UserSerializer()
    role = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()