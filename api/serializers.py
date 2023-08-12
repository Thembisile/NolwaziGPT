# serializers.py
from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    query = serializers.CharField()
    collection_name = serializers.CharField()
    
class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    collection_name = serializers.CharField()
