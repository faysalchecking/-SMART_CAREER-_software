from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Candidate(models.Model):
    """Core candidate model"""
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('SELECTED', 'Selected'),
        ('PROCESSING', 'Processing'),
        ('UNAVAILABLE', 'Unavailable'),
        ('DEPLOYED', 'Deployed'),
        ('BLOCKED', 'Blocked'),
        ('ARCHIVED', 'Archived'),
    ]

    # Primary fields
    candidate_id = models.CharField(max_length=20, unique=True, db_index=True)
    #photo = models.ImageField(upload_to='candidates/photos/', null=True, blank=True)
    
    # Personal information
    full_name = models.CharField(max_length=255, db_index=True)
    surname = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    
    # Contact information
    mobile = models.CharField(max_length=20, unique=True, db_index=True)
    alternative_mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    # Address information
    address = models.TextField(null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    upazila = models.CharField(max_length=100, null=True, blank=True)
    
    # Identity documents
    nid = models.CharField(max_length=50, unique=True, null=True, blank=True, db_index=True)
    passport_number = models.CharField(max_length=50, unique=True, db_index=True)
    passport_issue_date = models.DateField()
    passport_expiry_date = models.DateField()
    passport_issuing_country = models.CharField(max_length=100)
    
    # Qualifications
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    
    # Preferences
    preferred_country = models.CharField(max_length=100, null=True, blank=True)
    preferred_position = models.CharField(max_length=255, null=True, blank=True)
    
    # Relationships
    agent = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates')
    recruiter = models.ForeignKey('Recruiter', on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates')
    
    # Status
    source = models.CharField(max_length=100, default='Manual', null=True, blank=True)
    current_stage = models.CharField(max_length=50, null=True, blank=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    availability = models.CharField(max_length=100, null=True, blank=True)
    
    # Metadata
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='candidates_created')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['passport_number']),
            models.Index(fields=['mobile']),
            models.Index(fields=['full_name']),
            models.Index(fields=['current_status']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.candidate_id})"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        from dateutil.relativedelta import relativedelta
        today = timezone.now().date()
        return relativedelta(today, self.date_of_birth).years
    
    @property
    def passport_validity_days(self):
        """Days remaining for passport validity"""
        from datetime import date
        delta = self.passport_expiry_date - date.today()
        return delta.days
    
    @property
    def is_passport_expired(self):
        """Check if passport is expired"""
        from datetime import date
        return self.passport_expiry_date < date.today()
    
    @property
    def is_passport_expiring_soon(self):
        """Check if passport expiring within 90 days"""
        return 0 <= self.passport_validity_days <= 90


class Agent(models.Model):
    """Recruitment agent model"""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    agent_id = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    area_country = models.CharField(max_length=100, null=True, blank=True)
    license = models.CharField(max_length=100, null=True, blank=True)
    agreement_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['company_name']
    
    def __str__(self):
        return self.company_name


class Recruiter(models.Model):
    """Recruiter/Staff model"""
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='recruiter_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"