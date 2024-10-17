from django.db import models
from bookshelf.models import Book
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from accounts.tasks import send_email_async

User = get_user_model()

# Create your models here.
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=14))
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user']),  # For user lookups
            models.Index(fields=['book']),  # For book lookups
            models.Index(fields=['is_returned']),  # For filtering returned books
        ]

    def send_overdue_notification(self):
        """
        Sends an email notification to the user if the book is overdue.
        """
        subject = f"Overdue Book Notification: {self.book.title}"
        message = f"Dear {self.user.username},\n\nThe book '{self.book.title}' was due on {self.due_date}. Please return it as soon as possible."
        recipient_list = [self.user.email]
        
        # Call the Celery task to send the email asynchronously
        send_email_async.delay(subject, message, recipient_list)

    def check_overdue(self):

        if self.return_date is None and timezone.now() > self.due_date:
            self.is_returned = True
            self.send_overdue_notification()  # Send email if overdue
        return self.is_returned
    
    def save(self, *args, **kwargs): # If this is a new transaction (i.e., book being checked out)
        if not self.is_returned and self.book.available_copies <= 0:
            raise ValidationError("No copies available for this book.")
        
        # Reduce available copies on checkout
        if not self.is_returned:
            self.book.available_copies -= 1
            self.book.save()

        super(Loan, self).save(*args, **kwargs)
    
    def notify_book_available(self, book):
       
        subject = f"Book Available: {book.title}"
        message = f"Dear {self.user.username},\n\nThe book '{book.title}' is now available for checkout."
        recipient_list = [self.user.email]
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        book = models.ForeignKey(Book, on_delete=models.CASCADE)
        check_out_date = models.DateTimeField(auto_now_add=True)
        due_date = models.DateTimeField(default=timezone.now() + timedelta(days=14))
        return_date = models.DateTimeField(null=True, blank=True)
        is_returned = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user']),  # For user lookups
            models.Index(fields=['book']),  # For book lookups
            models.Index(fields=['is_returned']),  # For filtering returned books
        ]

    def send_overdue_notification(self):
        """
        Sends an email notification to the user if the book is overdue.
        """
        subject = f"Overdue Book Notification: {self.book.title}"
        message = f"Dear {self.user.username},\n\nThe book '{self.book.title}' was due on {self.due_date}. Please return it as soon as possible."
        recipient_list = [self.user.email]
        
        # Call the Celery task to send the email asynchronously
        send_email_async.delay(subject, message, recipient_list)

    def check_overdue(self):
        """
        Check if the transaction is overdue and send notification.
        """
        if self.return_date is None and timezone.now() > self.due_date:
            self.is_returned = True
            self.send_overdue_notification()  # Send email if overdue
        return self.is_returned
    
    def save(self, *args, **kwargs):
        # If this is a new transaction (i.e., book being checked out)
        if not self.is_returned and self.book.available_copies <= 0:
            raise ValidationError("No copies available for this book.")
        
        # Reduce available copies on checkout
        if not self.is_returned:
            self.book.available_copies -= 1
            self.book.save()

        super(Loan, self).save(*args, **kwargs)
    
    def notify_book_available(self, book):
        subject = f"Book Available: {book.title}"
        message = f"Dear {self.user.username},\n\nThe book '{book.title}' is now available for checkout."
        recipient_list = [self.user.email]
        
        # Call the Celery task to send the email asynchronously
        send_email_async.delay(subject, message, recipient_list)

    def __str__(self):
        return f'{self.book.title} checked out by {self.user.username}'
    
class Overdue(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    overdue_date = models.DateTimeField(auto_now_add=True)
    penalty_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Overdue record for {self.loan.book.title} by {self.loan.user.username}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    notification_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.notification_type}'

    def __str__(self):
        return f'{self.book.title} checked out by {self.user.username}'
    
class Overdue(models.Model):
    transaction = models.ForeignKey(Loan, on_delete=models.CASCADE)
    overdue_date = models.DateTimeField(auto_now_add=True)
    penalty_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Overdue record for {self.transaction.book.title} by {self.transaction.user.username}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    notification_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.notification_type}'