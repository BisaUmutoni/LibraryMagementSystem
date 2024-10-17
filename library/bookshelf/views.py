from django.shortcuts import render

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from rest_framework.filters import SearchFilter

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from accounts.permissions import  IsAdminOrUser, IsMember, PermitCheckoutBooks

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@swagger_auto_schema(tags=['Books'])

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrUser, IsMember, PermitCheckoutBooks]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author', 'isbn']
    filterset_fields = ['title', 'author', 'isbn']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'librarian']:
            return Book.objects.all()
        return Book.objects.filter(copies_available__gt=0)
    
    def perform_create(self, serializer):
        if self.request.user.role in ['admin', 'librarian']:
            serializer.save()
    
    def perform_update(self, serializer):
        if self.request.user.role in ['admin', 'librarian']:
            serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role in ['admin', 'librarian']:
            instance.delete()
