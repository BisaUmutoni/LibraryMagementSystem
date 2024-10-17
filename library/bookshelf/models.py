from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.
User = get_user_model()
class Book(models.Model): # Model to mange Book creation
    title = models.CharField(max_length=255)
    author = models.CharField(max_length= 200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateTimeField()
    publisher = models.CharField(max_length=255)
    copies_available = models.IntegerField()

    class Meta: # Order books by title 
        permissions = [
            ("can_borrow_books", "Can borrow books"),
            ("can_manage_books", "Can manage books"),
        ]
        
        indexes = [
            models.Index(fields=['published_date']),  # Index for date searches
        ]  

    def __str__(self):
        return  f"{self.title} by {self.author}"

    def reduce_copies(self):
        if self.copies_available > 0:
            self.copies_available -= 1
            if self.copies_available == 0:
                self.availability = False
            self.save()

    def increase_copies(self):
        self.copies_available += 1
        self.availability = True
        self.save()