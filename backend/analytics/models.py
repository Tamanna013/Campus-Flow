from mongoengine import (
    Document, StringField, DateTimeField, ListField, ReferenceField,
    IntField, FloatField, DictField
)
from datetime import datetime
import uuid

class EventAnalytics(Document):
    """Analytics for events"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    event = ReferenceField('events.Event', unique=True, required=True)
    
    # Views & Engagement
    total_views = IntField(default=0)
    total_registrations = IntField(default=0)
    total_attendance = IntField(default=0)
    total_shares = IntField(default=0)
    
    # Conversion
    registration_rate = FloatField(default=0)
    attendance_rate = FloatField(default=0)
    
    # Demographics
    attendee_departments = DictField(default={})  # {dept: count}
    attendee_years = DictField(default={})  # {'1st': count, ...}
    
    # Engagement
    average_session_duration = IntField(default=0)  # in seconds
    
    # Feedback
    average_rating = FloatField(default=0)
    total_reviews = IntField(default=0)
    
    # Cost analysis
    budget_utilization = FloatField(default=0)  # percentage
    cost_per_attendee = FloatField(null=True)
    
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'event_analytics',
    }
    
    class Meta:
        app_label = 'analytics'


class ClubAnalytics(Document):
    """Analytics for clubs"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    club = ReferenceField('clubs.Club', unique=True, required=True)
    
    # Membership
    total_members = IntField(default=0)
    new_members_this_month = IntField(default=0)
    retention_rate = FloatField(default=0)
    
    # Events
    total_events = IntField(default=0)
    total_attendees = IntField(default=0)
    average_attendance = IntField(default=0)
    
    # Engagement
    member_participation_rate = FloatField(default=0)
    average_event_rating = FloatField(default=0)
    
    # Growth
    growth_rate = FloatField(default=0)  # month over month
    
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'club_analytics',
    }
    
    class Meta:
        app_label = 'analytics'


class ResourceUtilization(Document):
    """Track resource usage statistics"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    resource = ReferenceField('resources.Resource', required=True)
    
    # Usage metrics
    total_bookings = IntField(default=0)
    approved_bookings = IntField(default=0)
    rejected_bookings = IntField(default=0)
    cancelled_bookings = IntField(default=0)
    
    # Time utilization
    hours_booked = IntField(default=0)
    hours_available = IntField(default=0)
    utilization_rate = FloatField(default=0)  # percentage
    
    # Peak usage
    peak_day = StringField(null=True)
    peak_hour = StringField(null=True)
    
    # Ratings
    average_rating = FloatField(default=0)
    total_ratings = IntField(default=0)
    
    # Maintenance impact
    maintenance_hours = IntField(default=0)
    downtime_percentage = FloatField(default=0)
    
    period_start = DateTimeField(required=True)
    period_end = DateTimeField(required=True)
    
    meta = {
        'collection': 'resource_utilization',
        'indexes': ['resource', 'period_start'],
    }
    
    class Meta:
        app_label = 'analytics'


class Report(Document):
    """Generated reports"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    name = StringField(required=True)
    description = StringField(null=True)
    
    # Report type
    report_type = StringField(choices=[
        ('events', 'Events Report'),
        ('clubs', 'Clubs Report'),
        ('resources', 'Resources Report'),
        ('users', 'Users Report'),
        ('custom', 'Custom Report'),
    ], required=True)
    
    # Data
    generated_by = ReferenceField('auth_app.User', required=True)
    data = DictField(required=True)
    
    # File
    file_path = StringField(null=True)
    file_type = StringField(choices=['csv', 'excel', 'pdf'], default='csv')
    file_size = IntField(null=True)
    
    # Period
    period_start = DateTimeField(required=True)
    period_end = DateTimeField(required=True)
    
    created_at = DateTimeField(default=datetime.utcnow)
    downloaded_count = IntField(default=0)
    
    meta = {
        'collection': 'reports',
        'indexes': ['report_type', 'created_at'],
    }
    
    class Meta:
        app_label = 'analytics'