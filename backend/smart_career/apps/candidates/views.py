from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Candidate, Agent, Recruiter
from .serializers import (
    CandidateListSerializer,
    CandidateDetailSerializer,
    CandidateCreateUpdateSerializer,
    AgentSerializer,
    RecruiterSerializer,
)

class CandidateViewSet(viewsets.ModelViewSet):
    """Candidate CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['current_status', 'nationality', 'agent', 'recruiter']
    search_fields = ['full_name', 'mobile', 'email', 'candidate_id', 'passport_number', 'nid']
    ordering_fields = ['created_at', 'full_name', 'current_status', 'passport_expiry_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CandidateDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CandidateCreateUpdateSerializer
        return CandidateListSerializer
    
    def get_queryset(self):
        return Candidate.objects.select_related('agent', 'recruiter', 'created_by').all()
    
    def create(self, request, *args, **kwargs):
        """Create new candidate"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return detail view after creation
        candidate = serializer.instance
        return Response(
            CandidateDetailSerializer(candidate).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change candidate status"""
        candidate = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Candidate.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        candidate.current_status = new_status
        candidate.save()
        
        return Response(
            CandidateDetailSerializer(candidate).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def expiring_passports(self, request):
        """Get candidates with passports expiring soon (90 days)"""
        candidates = Candidate.objects.filter(
            is_passport_expiring_soon=True
        ).values_list('id', flat=True)
        
        # This won't work as is_passport_expiring_soon is a property
        # Use raw SQL or recalculate in Python
        from datetime import date, timedelta
        today = date.today()
        ninety_days = today + timedelta(days=90)
        
        candidates = Candidate.objects.filter(
            passport_expiry_date__gte=today,
            passport_expiry_date__lte=ninety_days
        )
        
        serializer = CandidateListSerializer(candidates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expired_passports(self, request):
        """Get candidates with expired passports"""
        from datetime import date
        candidates = Candidate.objects.filter(passport_expiry_date__lt=date.today())
        serializer = CandidateListSerializer(candidates, many=True)
        return Response(serializer.data)

class AgentViewSet(viewsets.ModelViewSet):
    """Agent CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', 'email', 'phone']

class RecruiterViewSet(viewsets.ModelViewSet):
    """Recruiter CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    queryset = Recruiter.objects.select_related('user')
    serializer_class = RecruiterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']