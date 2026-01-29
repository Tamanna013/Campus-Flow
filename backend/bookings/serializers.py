from rest_framework import serializers
from bookings.models import Booking
from resources.serializers import ResourceSerializer
from auth_app.serializers import UserSerializer

class BookingSerializer(serializers.Serializer):
    """Booking serializer"""
    
    id = serializers.CharField(read_only=True)
    resource = ResourceSerializer(read_only=True)
    resource_id = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    duration_hours = serializers.IntegerField()
    purpose = serializers.CharField()
    status = serializers.CharField(read_only=True)
    expected_attendance = serializers.IntegerField(required=False)
    special_requirements = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        booking = Booking(**validated_data)
        
        # Check for conflicts
        if booking.has_conflict():
            raise serializers.ValidationError("Time slot is not available")
        
        booking.save()
        return booking