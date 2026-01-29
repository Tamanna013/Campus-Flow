from rest_framework import serializers
from clubs.models import Club, ClubMembership, ClubPermission
from auth_app.serializers import UserSerializer

class ClubSerializer(serializers.Serializer):
    """Club serializer"""
    
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField()
    category = serializers.CharField()
    logo = serializers.CharField(allow_null=True)
    banner = serializers.CharField(allow_null=True)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    website = serializers.CharField(required=False, allow_blank=True)
    instagram = serializers.CharField(required=False, allow_blank=True)
    facebook = serializers.CharField(required=False, allow_blank=True)
    discord = serializers.CharField(required=False, allow_blank=True)
    members_count = serializers.IntegerField(read_only=True)
    public_events_count = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    head = UserSerializer(read_only=True)
    
    def create(self, validated_data):
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['name'])
        club = Club(**validated_data)
        club.save()
        return club
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = datetime.utcnow()
        instance.save()
        return instance


class ClubMembershipSerializer(serializers.Serializer):
    """Club membership serializer"""
    
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)
    role = serializers.CharField()
    status = serializers.CharField()
    events_attended = serializers.IntegerField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        membership = ClubMembership(**validated_data)
        membership.save()
        return membership


class ClubListSerializer(serializers.Serializer):
    """Lightweight club serializer for lists"""
    
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    logo = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    members_count = serializers.IntegerField(read_only=True)