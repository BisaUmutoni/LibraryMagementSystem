from django.db import models
from django.conf import settings
from accounts.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length= 200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateTimeField()
    publisher = models.CharField(max_length=255)
    copies_available = models.IntegerField()

    def __str__(self):
        return self.title

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

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)  # True for active loan, False for returned

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user} on {self.borrow_date}"

    def return_book(self):
        self.return_date = models.DateTimeField(auto_now=True)
        self.status = False
        self.book.increase_copies()
        self.save()