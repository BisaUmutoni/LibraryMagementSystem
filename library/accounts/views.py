from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

   # Create a user
    def perform_create(self, serializer):
        serializer.save()

    # User Profile
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
# Custom auth token view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user=response.data['user'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'role': token.user.role
        })
def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

def profile_view(request):
    return render(request, 'accounts/profile.html')
