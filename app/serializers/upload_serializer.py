from rest_framework.serializers import Serializer, FileField, Field


class UploadSerializer(Serializer):
    name = Field()
    description = Field()
    source_file = FileField()
    target_file = FileField()
    class Meta:
        fields = ['source_file', 'target_file']