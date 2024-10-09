from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

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

# Loan View Set

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role == 'member':
            book = serializer.validated_data['book']
            if book.copies_available > 0:
                book.reduce_copies()
                serializer.save(user=self.request.user)