# accounts/urls.py
from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='profile'),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]


