from mongoengine import (
    Document, StringField, DateTimeField, ListField, ReferenceField,
    IntField, BooleanField, DictField, FloatField, EmbeddedDocument,
    EmbeddedDocumentField
)
from datetime import datetime
import uuid

class EventBudget(EmbeddedDocument):
    """Budget tracking for events"""
    total_amount = FloatField(required=True, default=0)
    currency = StringField(default='INR')
    spent_amount = FloatField(default=0)
    budget_items = ListField(DictField(), default=[])
    
    def remaining_budget(self):
        return self.total_amount - self.spent_amount


class Event(Document):
    """Event model"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('club_members', 'Club Members Only'),
        ('private', 'Private'),
    ]
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic Info
    title = StringField(required=True, max_length=200)
    description = StringField(required=True)
    short_description = StringField(null=True, max_length=300)
    
    # Dates & Location
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    location = StringField(required=True)
    location_coordinates = DictField(null=True)  # {lat, lng}
    
    # Organization
    organizer = ReferenceField('auth_app.User', required=True)
    clubs = ListField(ReferenceField('clubs.Club'), default=[])
    co_organizers = ListField(ReferenceField('auth_app.User'), default=[])
    
    # Budget
    budget = EmbeddedDocumentField(EventBudget, default=EventBudget())
    
    # Capacity & Registration
    max_capacity = IntField(null=True)
    current_attendance = IntField(default=0)
    registered_attendees = ListField(ReferenceField('auth_app.User'), default=[])
    allow_registration = BooleanField(default=True)
    
    # Status & Workflow
    status = StringField(choices=STATUS_CHOICES, default='draft')
    visibility = StringField(choices=VISIBILITY_CHOICES, default='public')
    is_collaborative = BooleanField(default=False)
    
    # Approval workflow
    submitted_at = DateTimeField(null=True)
    approved_by = ReferenceField('auth_app.User', null=True)
    approved_at = DateTimeField(null=True)
    rejection_reason = StringField(null=True)
    
    # Tags & Categories
    tags = ListField(StringField(), default=[])
    category = StringField(null=True)
    
    # Media
    poster_image = StringField(null=True)
    gallery_images = ListField(StringField(), default=[])
    event_link = StringField(null=True)  # For online events
    
    # Additional Info
    requirements = ListField(StringField(), default=[])
    rules = ListField(StringField(), default=[])
    
    # Metrics
    views_count = IntField(default=0)
    shares_count = IntField(default=0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    published_at = DateTimeField(null=True)
    
    meta = {
        'collection': 'events',
        'indexes': [
            'status',
            'organizer',
            'clubs',
            'start_date',
            'visibility',
        ],
    }
    
    def is_ongoing(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date
    
    def is_full(self):
        return self.max_capacity and self.current_attendance >= self.max_capacity
    
    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'events'


class EventCollaboration(Document):
    """Track collaboration between clubs in events"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    event = ReferenceField('events.Event', required=True)
    club = ReferenceField('clubs.Club', required=True)
    coordinator = ReferenceField('auth_app.User', required=True)
    
    # Contribution tracking
    contribution_description = StringField(null=True)
    is_co_organizer = BooleanField(default=False)
    
    # Approval
    status = StringField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    approved_at = DateTimeField(null=True)
    
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'event_collaborations',
    }
    
    class Meta:
        app_label = 'events'


class EventAttendance(Document):
    """Track event attendance"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    event = ReferenceField('events.Event', required=True)
    user = ReferenceField('auth_app.User', required=True)
    
    status = StringField(choices=[
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ], default='registered')
    
    registered_at = DateTimeField(default=datetime.utcnow)
    attended_at = DateTimeField(null=True)
    check_in_code = StringField(null=True)
    
    meta = {
        'collection': 'event_attendance',
        'unique_together': [('event', 'user')],
    }
    
    class Meta:
        app_label = 'events'