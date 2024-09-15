from django.urls import path, include
from rest_framework import routers
from .views import UploadView

# router = routers.DefaultRouter()
# router.register(r'upload', views.UploadViewSet, basename='upload')

urlpatterns = [
    path('upload', UploadView.as_view(), name="upload"),
]