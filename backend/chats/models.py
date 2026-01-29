from mongoengine import (
    Document, StringField, DateTimeField, ListField, ReferenceField,
    BooleanField, DictField, IntField
)
from datetime import datetime
import uuid

class ChatGroup(Document):
    """Group chat for clubs or events"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True, max_length=200)
    description = StringField(null=True)
    
    # Context
    type = StringField(choices=[
        ('club', 'Club Group'),
        ('event', 'Event Group'),
        ('committee', 'Committee Group'),
        ('project', 'Project Group'),
    ], required=True)
    
    # References
    club = ReferenceField('clubs.Club', null=True)
    event = ReferenceField('events.Event', null=True)
    
    # Members
    members = ListField(ReferenceField('auth_app.User'), required=True)
    admin = ReferenceField('auth_app.User', required=True)
    
    # Settings
    is_private = BooleanField(default=False)
    allow_file_sharing = BooleanField(default=True)
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'chat_groups',
        'indexes': ['club', 'event', 'members'],
    }
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'messages'


class Message(Document):
    """Individual message"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Sender
    sender = ReferenceField('auth_app.User', required=True)
    
    # Recipients
    receiver = ReferenceField('auth_app.User', null=True)  # For direct messages
    chat_group = ReferenceField('messages.ChatGroup', null=True)  # For group messages
    
    # Content
    content = StringField(required=True)
    message_type = StringField(choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('announcement', 'Announcement'),
    ], default='text')
    
    # File attachment
    attachment = DictField(null=True)  # {filename, url, type, size}
    
    # Status
    is_read = BooleanField(default=False)
    is_edited = BooleanField(default=False)
    
    # Reactions
    reactions = DictField(default={})  # {emoji: [user_ids]}
    
    # Context
    context = DictField(null=True)  # {type: 'event'/'club', id: ObjectId}
    
    # Threading
    reply_to = ReferenceField('messages.Message', null=True)  # For message threads
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'messages',
        'indexes': [
            'sender',
            'receiver',
            'chat_group',
            'created_at',
            ('sender', 'receiver'),
        ],
    }
    
    def __str__(self):
        return f"Message from {self.sender.get_full_name()}"
    
    class Meta:
        app_label = 'messages'


class Conversation(Document):
    """Track one-to-one conversations"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    participant1 = ReferenceField('auth_app.User', required=True)
    participant2 = ReferenceField('auth_app.User', required=True)
    
    # Metadata
    last_message = ReferenceField('messages.Message', null=True)
    last_message_at = DateTimeField(null=True)
    message_count = IntField(default=0)
    
    # Status
    is_muted_by = ListField(ReferenceField('auth_app.User'), default=[])
    is_archived_by = ListField(ReferenceField('auth_app.User'), default=[])
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'conversations',
        'indexes': [
            ('participant1', 'participant2'),
        ],
    }
    
    class Meta:
        app_label = 'messages'