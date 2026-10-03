from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer

class AuthenticationViewSet(viewsets.ViewSet):
    """Authentication endpoints"""
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login endpoint"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response({
            'user_id': user.id,
            'email': user.email,
            'message': 'Login successful'
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """User logout endpoint"""
        return Response({'message': 'Logout successful'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user info"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )