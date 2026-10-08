from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentTypeViewSet, PassportScanViewSet

app_name = 'documents'

router = DefaultRouter()
router.register(r'', DocumentViewSet, basename='document')
router.register(r'types', DocumentTypeViewSet, basename='document_type')
router.register(r'passport-scans', PassportScanViewSet, basename='passport_scan')

urlpatterns = [
    path('', include(router.urls)),
]