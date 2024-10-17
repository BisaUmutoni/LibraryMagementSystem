# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, LogoutViewSet, ProfileViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')  # Handles all user-related CRUD

urlpatterns = [
    path('', include(router.urls)),  # Include routes registered with the router
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),  # JWT Login
    path('logout/', LogoutViewSet.as_view({'post': 'create'}), name='logout'),  # JWT Logout
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),  # User Registration
    path('profile/', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='profile'),  # User Profile
]



