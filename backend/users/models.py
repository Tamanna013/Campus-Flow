from mongoengine import (
    Document, StringField, EmailField, BooleanField, DateTimeField,
    ListField, ReferenceField, DictField, IntField, FloatField,
    EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime
import uuid

class UserProfile(Document):
    """Extended user profile information"""
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('members_only', 'Club Members Only'),
    ]
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField('auth_app.User', unique=True, required=True)
    
    # Professional Info
    specialization = StringField(null=True)
    skills = ListField(StringField(), default=[])
    interests = ListField(StringField(), default=[])
    
    # Contact & Social
    linkedin_url = StringField(null=True)
    github_url = StringField(null=True)
    portfolio_url = StringField(null=True)
    
    # Visibility
    profile_visibility = StringField(choices=VISIBILITY_CHOICES, default='public')
    show_email = BooleanField(default=False)
    show_phone = BooleanField(default=False)
    
    # Activity metrics
    total_events_attended = IntField(default=0)
    total_events_organized = IntField(default=0)
    clubs_joined = ListField(ReferenceField('clubs.Club'), default=[])
    clubs_heading = ListField(ReferenceField('clubs.Club'), default=[])
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'user_profiles',
        'indexes': ['user', 'profile_visibility'],
    }
    
    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"
    
    class Meta:
        app_label = 'users'