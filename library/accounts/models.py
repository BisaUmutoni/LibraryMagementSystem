from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# USER Manager.
class CustomUserManager(BaseUserManager): #  Create a regular user
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.role = 'admin'  # Set role to admin
        user.save(using=self._db)
        return user

# Creating an Abstract Custom User base model for the user to define common fiels and functionalities for all users Admina and Librarian
class User(AbstractBaseUser, PermissionsMixin): 
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    date_of_membership = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # determine if user is active
    is_staff = models.BooleanField(default=False) # determine if user is hass access to admin interface or not

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    # Adding related_name to avoid reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Avoid clash with Django's default User model
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Avoid clash with Django's default User model
        blank=True
    )


    USERNAME_FIELD = 'username' # The unique identifier for the user during authentication is the email
    REQUIRED_FIELDS = ['email'] # Additional required fields when creating a user via 

    objects = CustomUserManager()

    def __str__(self):
        return self.username








        
         
