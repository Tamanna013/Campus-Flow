from mongoengine import (
    Document, StringField, DateTimeField, ListField, ReferenceField,
    IntField, BooleanField, DictField, FloatField
)
from datetime import datetime
import uuid

class Booking(Document):
    """Resource booking model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Core Info
    resource = ReferenceField('resources.Resource', required=True)
    user = ReferenceField('auth_app.User', required=True)
    event = ReferenceField('events.Event', null=True)
    
    # Timing
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    duration_hours = IntField(required=True)
    
    # Purpose
    purpose = StringField(required=True, max_length=500)
    expected_attendance = IntField(null=True)
    
    # Status & Workflow
    status = StringField(choices=STATUS_CHOICES, default='pending')
    
    # Approval workflow
    submitted_at = DateTimeField(default=datetime.utcnow)
    approved_by = ReferenceField('auth_app.User', null=True)
    approved_at = DateTimeField(null=True)
    rejection_reason = StringField(null=True)
    
    # Additional Info
    special_requirements = StringField(null=True)
    notes = StringField(null=True)
    
    # Status flags
    is_recurring = BooleanField(default=False)
    recurrence_rule = StringField(null=True)  # RRULE format
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField(null=True)
    cancelled_at = DateTimeField(null=True)
    
    meta = {
        'collection': 'bookings',
        'indexes': [
            'resource',
            'user',
            'status',
            'start_date',
            'event',
        ],
    }
    
    def has_conflict(self):
        """Check if booking has time conflict with approved bookings"""
        conflicting = Booking.objects(
            resource=self.resource,
            status='approved',
            id__ne=self.id,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        )
        return conflicting.count() > 0
    
    def __str__(self):
        return f"{self.resource.name} - {self.user.get_full_name()}"
    
    class Meta:
        app_label = 'bookings'


class BookingRejectionLog(Document):
    """Track rejected bookings"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    booking = ReferenceField('bookings.Booking', required=True)
    reason = StringField(required=True)
    rejected_by = ReferenceField('auth_app.User', required=True)
    rejected_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'booking_rejection_logs',
    }
    
    class Meta:
        app_label = 'bookings'