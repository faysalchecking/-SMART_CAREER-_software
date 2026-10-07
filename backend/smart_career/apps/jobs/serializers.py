from rest_framework import serializers
from .models import Job, Employer

class EmployerSerializer(serializers.ModelSerializer):
    """Serialize employer information"""
    class Meta:
        model = Employer
        fields = ['id', 'employer_id', 'company_name', 'country', 'email', 'phone', 'status']

class JobListSerializer(serializers.ModelSerializer):
    """Serialize job for list view"""
    employer_name = serializers.CharField(source='employer.company_name', read_only=True)
    available_positions = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'job_id', 'title', 'country', 'city', 'salary_min', 'salary_max',
            'currency', 'quantity', 'filled_count', 'available_positions', 'status',
            'employer_name', 'experience_years', 'application_deadline', 'created_at'
        ]
        read_only_fields = ['id', 'job_id', 'available_positions', 'created_at']

class JobDetailSerializer(serializers.ModelSerializer):
    """Serialize job for detail view"""
    employer = EmployerSerializer(read_only=True)
    available_positions = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'job_id', 'title', 'description', 'employer', 'country', 'city',
            'salary_min', 'salary_max', 'currency', 'salary_period', 'quantity',
            'filled_count', 'available_positions', 'age_min', 'age_max', 'gender',
            'education', 'experience_years', 'languages', 'certification',
            'passport_validity_months', 'accommodation', 'food', 'transportation',
            'other_benefits', 'working_hours', 'overtime_allowed',
            'contract_period_months', 'visa_type', 'visa_sponsor', 'posting_date',
            'application_deadline', 'interview_date', 'status', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'job_id', 'available_positions', 'created_at', 'updated_at']

class JobCreateUpdateSerializer(serializers.ModelSerializer):
    """Serialize job for create/update"""
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'employer', 'country', 'city', 'salary_min',
            'salary_max', 'currency', 'salary_period', 'quantity', 'age_min', 'age_max',
            'gender', 'education', 'experience_years', 'languages', 'certification',
            'passport_validity_months', 'accommodation', 'food', 'transportation',
            'other_benefits', 'working_hours', 'overtime_allowed', 'contract_period_months',
            'visa_type', 'visa_sponsor', 'application_deadline', 'interview_date',
            'status', 'is_active', 'notes'
        ]
    
    def create(self, validated_data):
        # Generate job_id
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d')
        job_count = Job.objects.filter(job_id__startswith=f"JOB-{timestamp}").count()
        validated_data['job_id'] = f"JOB-{timestamp}-{job_count + 1:04d}"
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)