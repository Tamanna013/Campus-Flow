from rest_framework import serializers
from events.models import Event, EventCollaboration, EventAttendance
from auth_app.serializers import UserSerializer

class EventSerializer(serializers.Serializer):
    """Event serializer"""
    
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    short_description = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    location = serializers.CharField()
    status = serializers.CharField()
    visibility = serializers.CharField()
    max_capacity = serializers.IntegerField(required=False, allow_null=True)
    current_attendance = serializers.IntegerField(read_only=True)
    allow_registration = serializers.BooleanField()
    budget = serializers.DictField(required=False)
    poster_image = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    organizer = UserSerializer(read_only=True)
    
    def create(self, validated_data):
        event = Event(**validated_data)
        event.save()
        return event
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = datetime.utcnow()
        instance.save()
        return instance


class EventListSerializer(serializers.Serializer):
    """Lightweight event serializer for lists"""
    
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    location = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    current_attendance = serializers.IntegerField(read_only=True)
    poster_image = serializers.CharField(read_only=True)
    organizer = UserSerializer(read_only=True)