from mongoengine import (
    Document, StringField, DateTimeField, ListField, ReferenceField,
    IntField, BooleanField, DictField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime
import uuid

class AvailabilitySlot(EmbeddedDocument):
    """Availability slot for resources"""
    day_of_week = StringField(required=True)  # Monday, Tuesday, etc.
    start_time = StringField(required=True)  # HH:MM format
    end_time = StringField(required=True)
    is_available = BooleanField(default=True)


class Resource(Document):
    """Resource model (rooms, equipment, labs)"""
    
    TYPE_CHOICES = [
        ('room', 'Room/Hall'),
        ('equipment', 'Equipment'),
        ('lab', 'Laboratory'),
        ('ground', 'Ground/Field'),
        ('other', 'Other'),
    ]
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic Info
    name = StringField(required=True, max_length=200)
    slug = StringField(unique=True, required=True)
    description = StringField(required=True)
    type = StringField(choices=TYPE_CHOICES, required=True)
    
    # Location
    location = StringField(required=True)
    building = StringField(null=True)
    room_number = StringField(null=True)
    floor = IntField(null=True)
    
    # Capacity
    capacity = IntField(null=True)  # for rooms
    quantity = IntField(default=1)  # for equipment
    
    # Features
    features = ListField(StringField(), default=[])  # e.g., 'projector', 'wifi', 'ac'
    
    # Availability
    availability_slots = ListField(EmbeddedDocumentField(AvailabilitySlot), default=[])
    
    # Booking Policy
    require_approval = BooleanField(default=True)
    advance_booking_days = IntField(default=7)  # How far in advance can be booked
    max_duration_hours = IntField(default=8)
    
    # Contact
    manager_name = StringField(null=True)
    manager_email = StringField(null=True)
    manager_phone = StringField(null=True)
    
    # Images
    images = ListField(StringField(), default=[])
    
    # Status
    is_active = BooleanField(default=True)
    
    # Usage metrics
    total_bookings = IntField(default=0)
    utilization_percentage = IntField(default=0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'resources',
        'indexes': ['type', 'location', 'is_active'],
    }
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'resources'


class ResourceMaintenanceLog(Document):
    """Track maintenance history"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    resource = ReferenceField('resources.Resource', required=True)
    
    maintenance_type = StringField(choices=[
        ('scheduled', 'Scheduled'),
        ('emergency', 'Emergency'),
        ('repair', 'Repair'),
    ])
    
    description = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(null=True)
    
    is_completed = BooleanField(default=False)
    
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'resource_maintenance_logs',
    }
    
    class Meta:
        app_label = 'resources'