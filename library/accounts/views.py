from django.shortcuts import render
from rest_framework import status, viewsets,  permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import filters
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer, LogoutSerializer

from django.contrib.auth import get_user_model

#from loans.models import loans


User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user accounts with role-based access.
    Admin users can perform CRUD operations on all users.
    Regular users can view and update their own profile.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]  # JWT to be applied at global level
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['username', 'email']
    ordering = ['id']
    search_fields = ['username', 'email']  # Search users by username or email

    def get_permissions(self):
        """Apply different permissions based on the user's role and request type."""
        if self.action in ['list', 'destroy']:
            return [permissions.IsAdminUser()]  # Only admins can list or delete users
        return super().get_permissions()
    def get_queryset(self):
        """Restrict access: Admins see all users, members only see their own profile."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        A custom action to retrieve the authenticated user's profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def change_role(self, request, pk=None):
        """
        Allow admin to change the role of a user.
        """
        user = self.get_object()
        new_role = request.data.get('role')
        if new_role not in ['admin', 'member']:
            return Response({'error': 'Invalid role provided'}, status=status.HTTP_400_BAD_REQUEST)

        user.role = new_role
        user.save()
        return Response({'message': f'User role changed to {new_role}'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reset_token(self, request, pk=None):
        """
        Allow a user to reset their JWT token (refresh and access).
        """
        user = self.get_object()
        if user != request.user and not request.user.is_staff:
            return Response({'error': 'You are not authorized to reset this token'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        """Ensure that only the authenticated user or admins can update profiles."""
        if self.request.user.is_staff or self.request.user == serializer.instance:
            serializer.save()
        else:
            raise permissions.PermissionDenied('You can only update your own profile.')

    def destroy(self, request, *args, **kwargs):
        """Override the delete method to prevent non-admins from deleting accounts."""
        user = self.get_object()
        if not request.user.is_staff:
            return Response({'error': 'Only admins can delete users'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class RegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Restrict access: Admins see all users, members only see their own profile."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
@action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])


class LoginViewSet(viewsets.ViewSet):
    """
    API endpoi nt for user login, providing JWT access.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutViewSet(viewsets.ViewSet):
    """
    API endpoint for user logout, invalidating the JWT refresh token.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for retrieving and updating user profiles.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow users to view only their own profile, admins can view all profiles.
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
