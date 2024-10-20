# library/loans/serializers.py

from rest_framework import serializers
from .models import Loan, Overdue, Notification

class LoanSerializer(serializers.ModelSerializer): # converts Loan model instance to JSON and vice versa.
    book_title = serializers.CharField(source='book.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'book_title', 'username', 
                  'check_out_date', 'due_date', 'return_date', 'is_returned']
        read_only_fields = ['check_out_date', 'return_date', 'is_returned']

    def validate(self, attrs):
            """Ensure that a user cannot check out a book if already checked out."""
            user = attrs.get('user')
            book = attrs.get('book')
            
            if Loan.objects.filter(user=user, book=book, is_returned=False).exists():
                raise serializers.ValidationError("You already have this book checked out.")
            
            return attrs


class OverdueSerializer(serializers.ModelSerializer):
    """Serializer for Overdue records."""
    class Meta:
        model = Overdue
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notifications."""
    class Meta:
        model = Notification
        fields = '__all__'