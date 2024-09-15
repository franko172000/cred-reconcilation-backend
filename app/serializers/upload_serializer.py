from rest_framework.serializers import Serializer, FileField, Field, ModelSerializer, SerializerMethodField

from app.models import Upload, Record


class RecordSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class UploadSerializer(ModelSerializer):
    record_count = SerializerMethodField()

    class Meta:
        model = Upload
        fields = ['id', 'title', 'description', 'source_file', 'target_file', 'discrepancies', 'missing_in_source',
                  'missing_in_target', 'record_count']

    def get_record_count(self, obj) -> int:
        return obj.record_set.count()


class UploadListSerializer(UploadSerializer):
    record_set = RecordSerializer(many=True, read_only=True)
    class Meta:
        model = Upload
        fields = ['id', 'title', 'description', 'source_file', 'target_file', 'discrepancies', 'missing_in_source',
                  'missing_in_target', 'record_set']
