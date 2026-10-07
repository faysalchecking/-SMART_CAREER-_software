from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, EmployerViewSet

app_name = 'jobs'

router = DefaultRouter()
router.register(r'', JobViewSet, basename='job')
router.register(r'employers', EmployerViewSet, basename='employer')

urlpatterns = [
    path('', include(router.urls)),
]