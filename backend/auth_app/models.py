from mongoengine import (
    Document, StringField, EmailField, BooleanField, DateTimeField,
    ListField, ReferenceField, DictField, IntField, FloatField
)
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import uuid
import jwt
from decouple import config

class User(Document):
    """Custom User model for MongoDB"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('organizer', 'Organizer/Club Head'),
        ('participant', 'Participant/Member'),
    ]
    
    PERMISSION_LEVELS = {
        'admin': ['create_club', 'manage_users', 'approve_events', 'manage_resources', 'view_analytics'],
        'organizer': ['create_event', 'manage_event', 'book_resource'],
        'participant': ['register_event', 'view_resources'],
    }
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    email = EmailField(unique=True, required=True)
    password_hash = StringField(required=True)
    first_name = StringField(required=True, max_length=100)
    last_name = StringField(required=True, max_length=100)
    department = StringField(null=True, max_length=100)
    year = StringField(null=True, choices=['1st', '2nd', '3rd', '4th', '5th'])
    role = StringField(choices=ROLE_CHOICES, default='participant')
    profile_picture = StringField(null=True)
    bio = StringField(null=True)
    phone = StringField(null=True)
    
    # Status flags
    is_active = BooleanField(default=True)
    is_verified = BooleanField(default=False)
    verification_token = StringField(null=True)
    verification_token_expires = DateTimeField(null=True)
    
    # OAuth
    oauth_providers = ListField(DictField(), default=[])
    
    # Preferences
    notification_preferences = DictField(default={
        'email_on_event_approval': True,
        'email_on_booking_status': True,
        'email_on_reminder': True,
        'in_app_notifications': True,
    })
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField(null=True)
    
    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'is_active',
            'role',
        ],
    }
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = make_password(password)
        self.save()
    
    def check_password(self, password):
        """Verify password"""
        return check_password(password, self.password_hash)
    
    def get_full_name(self):
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_permissions(self):
        """Get permissions based on role"""
        return self.PERMISSION_LEVELS.get(self.role, [])
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        return permission in self.get_permissions()
    
    def generate_verification_token(self):
        """Generate email verification token"""
        token = jwt.encode(
            {'user_id': self.id, 'exp': datetime.utcnow()},
            config('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
        self.verification_token = token
        self.save()
        return token
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    class Meta:
        app_label = 'auth_app'


class OAuthProvider(Document):
    """OAuth provider configuration"""
    
    name = StringField(required=True, unique=True)  # google, github, microsoft
    client_id = StringField(required=True)
    client_secret = StringField(required=True)
    authorize_url = StringField(required=True)
    token_url = StringField(required=True)
    user_info_url = StringField(required=True)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'oauth_providers',
    }
    
    class Meta:
        app_label = 'auth_app'