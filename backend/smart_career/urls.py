"""
URL configuration for SMART CAREER project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Token endpoints
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App endpoints
    path('api/auth/', include('smart_career.apps.authentication.urls', namespace='auth')),
    path('api/candidates/', include('smart_career.apps.candidates.urls', namespace='candidates')),
    path('api/jobs/', include('smart_career.apps.jobs.urls', namespace='jobs')),
    path('api/applications/', include('smart_career.apps.applications.urls', namespace='applications')),
    path('api/documents/', include('smart_career.apps.documents.urls', namespace='documents')),
    path('api/medical/', include('smart_career.apps.medical.urls', namespace='medical')),
    path('api/visa/', include('smart_career.apps.visa.urls', namespace='visa')),
    path('api/finance/', include('smart_career.apps.finance.urls', namespace='finance')),
    path('api/ai/', include('smart_career.apps.ai.urls', namespace='ai')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)