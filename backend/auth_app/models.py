from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """Custom User model for SQLite/PostgreSQL"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('organizer', 'Organizer/Club Head'),
        ('participant', 'Participant/Member'),
    ]
    
    # We use email as the username for login
    email = models.EmailField(unique=True)
    
    # Custom fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(
        max_length=10, 
        null=True, 
        blank=True, 
        choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th')]
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    phone = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    # Status flags
    is_verified = models.BooleanField(default=False)

    # Use email for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

# If you need OAuth later, create it as a standard Model
class OAuthProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)