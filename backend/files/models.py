from mongoengine import (
    Document, StringField, DateTimeField, ReferenceField,
    IntField, BooleanField, DictField, FloatField
)
from datetime import datetime
import uuid

class FileUpload(Document):
    """Track uploaded files"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # File Info
    original_filename = StringField(required=True)
    stored_filename = StringField(required=True)
    file_path = StringField(required=True)
    file_size = IntField(required=True)
    file_type = StringField(required=True)  # MIME type
    
    # Uploader
    uploaded_by = ReferenceField('auth_app.User', required=True)
    
    # Context
    context_type = StringField(null=True)  # 'event', 'club', 'resource'
    context_id = StringField(null=True)
    
    # Metadata
    is_public = BooleanField(default=False)
    is_archived = BooleanField(default=False)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'file_uploads',
        'indexes': ['uploaded_by', 'context_type', 'created_at'],
    }
    
    def get_file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)
    
    class Meta:
        app_label = 'files'