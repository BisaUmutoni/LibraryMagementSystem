from rest_framework import serializers
from .models import Book

from accounts.serializers import CustomUserSerializer
#from loans.serializers import LoanSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'publisher', 'copies_available']
        
        swagger_schema_fields = {
            "title": "Book",
            "description": "A book in the library system",
            "required": ["title", "author", "isbn", "published_date", "publisher"],
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64",
                    "readOnly": True,
                    "description": "Unique identifier for the book"
                },
                "title": {
                    "type": "string",
                    "maxLength": 200,
                    "description": "The title of the book"
                },
                "author": {
                    "type": "string",
                    "maxLength": 200,
                    "description": "The author of the book"
                },
                "isbn": {
                    "type": "string",
                    "maxLength": 13,
                    "minLength": 13,
                    "description": "The ISBN of the book (must be exactly 13 characters)"
                },
                "published_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The publication date of the book"
                },
                "publisher": {
                    "type": "string",
                    "maxLength": 255,
                    "description": "The book publisher"
                },
                "copies_available": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "The number of copies available for checkout"
                }
            }
        }
    def validate_isbn(self,value):
        if Book.objects.filter(isbn=value).exists() and len(value) != 13:
            raise serializers.ValidationError("ISBN must be unique and less than 13 characters.")
        return value
class BookStatusSerializer(serializers.ModelSerializer):
    # Serializer for the status of a book, full information including loans
   # current_loan = LoanSerializer(many=True, read_only=True)
    class Meta:
        fields = BookSerializer.Meta.fields = ['current_loan']