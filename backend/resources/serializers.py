from rest_framework import serializers

# A basic placeholder serializer to stop the crash
class ResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    
    # Add other fields here based on what your 
    # booking system expects from a 'Resource'