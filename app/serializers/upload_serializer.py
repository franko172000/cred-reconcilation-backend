from rest_framework.serializers import Serializer, FileField, Field, ModelSerializer

from app.models import Upload, Record


class RecordSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class UploadSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class UploadListSerializer(UploadSerializer):
    record_set = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Upload
        fields = ['id', 'title', 'description', 'source_file', 'target_file', 'discrepancies', 'missing_in_source',
                  'missing_in_target', 'record_set']
