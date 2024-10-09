from rest_framework import serializers
from .models import Book, Loan
from accounts.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'publisher', 'copies_available']

    def validate_isbn(self,value):
        if Book.objects.filter(isbn=value).exists() and len(value) != 13:
            raise serializers.ValidationError("ISBN must be unique and less than 13 characters.")
        return value

class LoanSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field='title', queryset=Book.objects.all())
    user = UserSerializer(read_only=True)  # Shows user info

    class Meta:
        model = Loan
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date', 'status']
        

    def validate_book(self, data): # to ensure a book can only be checked out if copies are available
        book = data['book']
        # Check if the book exists
        if not book:
            raise serializers.ValidationError("Book not found.")
        
        # Check if the book has been borrowed already
        if Loan.objects.filter(book=book, status='Borrowed').exists() and book.copies_available <= 0:
            raise serializers.ValidationError("No more copies.")
        return data
  

    def create(self, validated_data): # create method to handle book checkout
        book = validated_data['book']
        book.reduce_copies()  # Reduce the copies
        return super().create(validated_data)
