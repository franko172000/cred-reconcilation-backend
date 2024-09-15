from rest_framework.serializers import Serializer, FileField


class UploadSerializer(Serializer):
    source_file = FileField()
    target_file = FileField()
    class Meta:
        fields = ['source_file', 'target_file']