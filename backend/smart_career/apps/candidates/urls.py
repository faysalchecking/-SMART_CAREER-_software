from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, AgentViewSet, RecruiterViewSet

app_name = 'candidates'

router = DefaultRouter()
router.register(r'', CandidateViewSet, basename='candidate')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'recruiters', RecruiterViewSet, basename='recruiter')

urlpatterns = [
    path('', include(router.urls)),
]