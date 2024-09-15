from django.http import JsonResponse
from django.shortcuts import render
from injector import inject
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import upload_serializer
from .service import reconciliation_service
from rest_framework.parsers import MultiPartParser


# Create your views here.
class UploadView(GenericAPIView):
    serializer_class = upload_serializer.UploadSerializer
    parser_classes = [MultiPartParser]

    def get(self, request):
        return Response("GET API")

    def post(self, request, *args, **kwargs):
        reconcile_service = reconciliation_service.ReconciliationService()
        source_file = request.FILES.get('source_file')
        print(request.FILES)
        target_file = request.FILES.get('target_file')
        data = reconcile_service.reconcile(source_file, target_file)

        return Response(data)

