from rest_framework.serializers import Serializer, FileField, Field, ModelSerializer

from app.models import Upload


class UploadSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = ['source_file', 'target_file', 'title', 'description']