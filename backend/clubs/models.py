from mongoengine import (
    Document, StringField, DateTimeField, ListField, ReferenceField,
    IntField, BooleanField, DictField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime
import uuid

class Club(Document):
    """Club/Committee model"""
    
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('technical', 'Technical'),
        ('social', 'Social'),
        ('professional', 'Professional'),
        ('other', 'Other'),
    ]
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True, unique=True, max_length=200)
    slug = StringField(unique=True, required=True)
    description = StringField(required=True)
    logo = StringField(null=True)
    banner = StringField(null=True)
    category = StringField(choices=CATEGORY_CHOICES, required=True)
    
    # Leadership
    head = ReferenceField('auth_app.User', null=True)
    co_heads = ListField(ReferenceField('auth_app.User'), default=[])
    
    # Contact
    email = StringField(null=True)
    phone = StringField(null=True)
    website = StringField(null=True)
    
    # Social
    instagram = StringField(null=True)
    facebook = StringField(null=True)
    discord = StringField(null=True)
    
    # Stats
    members_count = IntField(default=0)
    public_events_count = IntField(default=0)
    
    # Status
    is_active = BooleanField(default=True)
    is_verified = BooleanField(default=False)
    
    # Metadata
    founded_year = IntField(null=True)
    meeting_schedule = StringField(null=True)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'clubs',
        'indexes': ['slug', 'category', 'is_active'],
    }
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'clubs'


class ClubMembership(Document):
    """Club membership model"""
    
    ROLE_CHOICES = [
        ('head', 'Head'),
        ('coordinator', 'Coordinator'),
        ('member', 'Member'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
        ('rejected', 'Rejected'),
    ]
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = ReferenceField('auth_app.User', required=True)
    club = ReferenceField('clubs.Club', required=True)
    role = StringField(choices=ROLE_CHOICES, default='member')
    status = StringField(choices=STATUS_CHOICES, default='active')
    
    # Permissions specific to this membership
    permissions = ListField(StringField(), default=[])
    
    # Metrics
    events_attended = IntField(default=0)
    last_active = DateTimeField(null=True)
    
    # Timestamps
    joined_at = DateTimeField(default=datetime.utcnow)
    left_at = DateTimeField(null=True)
    
    meta = {
        'collection': 'club_memberships',
        'indexes': [
            ('user', 'club'),
            'status',
            'role',
        ],
        'unique_together': [('user', 'club')],
    }
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.club.name}"
    
    class Meta:
        app_label = 'clubs'


class ClubPermission(Document):
    """Define permissions for club roles"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    role = StringField(required=True, unique=True)  # 'head', 'coordinator', 'member'
    permissions = ListField(StringField(), default=[])
    
    AVAILABLE_PERMISSIONS = [
        'create_event',
        'edit_event',
        'delete_event',
        'approve_event',
        'manage_members',
        'book_resource',
        'manage_club_info',
        'send_announcement',
        'view_analytics',
    ]
    
    meta = {
        'collection': 'club_permissions',
    }
    
    class Meta:
        app_label = 'clubs'