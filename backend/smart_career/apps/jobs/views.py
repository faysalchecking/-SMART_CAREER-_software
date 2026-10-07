from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Employer
from .serializers import (
    JobListSerializer,
    JobDetailSerializer,
    JobCreateUpdateSerializer,
    EmployerSerializer,
)

class JobViewSet(viewsets.ModelViewSet):
    """Job CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'country', 'employer', 'is_active']
    search_fields = ['title', 'job_id', 'description']
    ordering_fields = ['posting_date', 'application_deadline', 'salary_max']
    ordering = ['-posting_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return JobCreateUpdateSerializer
        return JobListSerializer
    
    def get_queryset(self):
        return Job.objects.select_related('employer', 'created_by').all()
    
    def create(self, request, *args, **kwargs):
        """Create new job"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return detail view after creation
        job = serializer.instance
        return Response(
            JobDetailSerializer(job).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close job posting"""
        job = self.get_object()
        job.status = 'CLOSED'
        job.save()
        return Response(JobDetailSerializer(job).data)
    
    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Reopen job posting"""
        job = self.get_object()
        job.status = 'OPEN'
        job.save()
        return Response(JobDetailSerializer(job).data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all open jobs with available positions"""
        jobs = Job.objects.filter(
            status='OPEN',
            is_active=True,
            quantity__gt=models.F('filled_count')
        )
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)

class EmployerViewSet(viewsets.ModelViewSet):
    """Employer CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', 'email', 'country']