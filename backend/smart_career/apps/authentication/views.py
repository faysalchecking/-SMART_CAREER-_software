from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import (
    LoginSerializer,
    LoginResponseSerializer,
    MeSerializer,
    UserSerializer,
    UserProfileSerializer,
)

class AuthenticationViewSet(viewsets.ViewSet):
    """Authentication endpoints"""

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        User login endpoint
        
        Request body:
        {
            "email": "admin@smartcareer.com",
            "password": "password123"
        }
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Prepare response data
        response_data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """User logout endpoint"""
        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user information"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            data = {
                'user': UserSerializer(request.user).data,
                'role': profile.role,
                'phone': profile.phone,
                'address': profile.address,
            }
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def refresh(self, request):
        """
        Refresh JWT token
        
        Request body:
        {
            "refresh": "refresh_token_here"
        }
        """
        from rest_framework_simplejwt.views import TokenRefreshView
        
        refresh_view = TokenRefreshView.as_view()
        return refresh_view(request)