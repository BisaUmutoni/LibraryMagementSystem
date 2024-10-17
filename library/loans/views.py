from django.shortcuts import render
from .models import Loan
from rest_framework import viewsets, status, filters, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import LoanSerializer

# Create your views here.
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