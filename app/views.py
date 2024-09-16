from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Upload
from .serializers import upload_serializer
from .service import reconciliation_service


# Create your views here.
class UploadView(GenericAPIView):
    serializer_class = upload_serializer.UploadSerializer
    parser_classes = [MultiPartParser]
    queryset = Upload.objects.all().order_by('-id')

    def get(self, request):
        serializer = self.serializer_class(Upload.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        reconcile_service = reconciliation_service.ReconciliationService()
        data = reconcile_service.reconcile(request.data)
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UploadDetailView(RetrieveAPIView):
    serializer_class = upload_serializer.UploadListSerializer
    parser_classes = [MultiPartParser]
    queryset = Upload.objects.all().prefetch_related('record_set')
