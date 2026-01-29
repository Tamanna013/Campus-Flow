from rest_framework import serializers
from auth_app.models import User
import jwt
from decouple import config
from datetime import datetime, timedelta

class UserRegisterSerializer(serializers.Serializer):
    """Serializer for user registration"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    department = serializers.CharField(required=False, allow_blank=True)
    year = serializers.CharField(required=False)
    
    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return data
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            department=validated_data.get('department'),
            year=validated_data.get('year'),
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Send verification email
        from django.core.mail import send_mail
        verification_token = user.generate_verification_token()
        send_mail(
            'Email Verification',
            f'Click here to verify: {config("FRONTEND_URL")}/verify/{verification_token}',
            config('DEFAULT_FROM_EMAIL'),
            [user.email],
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")
        
        data['user'] = user
        return data


class TokenObtainSerializer(serializers.Serializer):
    """Return access and refresh tokens"""
    
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class UserSerializer(serializers.Serializer):
    """Basic user serializer"""
    
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    department = serializers.CharField(allow_blank=True)
    year = serializers.CharField(allow_blank=True)
    role = serializers.CharField(read_only=True)
    profile_picture = serializers.CharField(allow_null=True)
    bio = serializers.CharField(allow_blank=True, allow_null=True)
    phone = serializers.CharField(allow_blank=True, allow_null=True)
    is_verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.department = validated_data.get('department', instance.department)
        instance.year = validated_data.get('year', instance.year)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.updated_at = datetime.utcnow()
        instance.save()
        return instance


class EmailVerificationSerializer(serializers.Serializer):
    """Verify email token"""
    
    token = serializers.CharField()
    
    def validate_token(self, value):
        try:
            payload = jwt.decode(value, config('JWT_SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return {'user': user, 'token': value}
        except:
            raise serializers.ValidationError("Invalid or expired token")


class PasswordChangeSerializer(serializers.Serializer):
    """Change password"""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data.pop('new_password_confirm'):
            raise serializers.ValidationError({"new_password": "Passwords don't match"})
        return data