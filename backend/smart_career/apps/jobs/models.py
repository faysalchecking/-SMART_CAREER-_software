from django.db import models
from django.core.validators import MinValueValidator

class Job(models.Model):
    """Job/Demand model"""
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('ON_HOLD', 'On Hold'),
        ('FILLED', 'Filled'),
        ('CANCELLED', 'Cancelled'),
    ]

    # Job information
    job_id = models.CharField(max_length=20, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    # Employer/Client
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='jobs')
    
    # Location
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    
    # Compensation
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    salary_period = models.CharField(
        max_length=20,
        choices=[('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')],
        default='MONTHLY'
    )
    
    # Demand
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    filled_count = models.IntegerField(default=0)
    
    # Requirements
    age_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(18)])
    age_max = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('ANY', 'Any'), ('MALE', 'Male'), ('FEMALE', 'Female')],
        default='ANY'
    )
    education = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    languages = models.TextField(null=True, blank=True)
    certification = models.TextField(null=True, blank=True)
    
    # Passport requirement
    passport_validity_months = models.IntegerField(default=6, validators=[MinValueValidator(1)])
    
    # Benefits
    accommodation = models.CharField(max_length=255, null=True, blank=True)
    food = models.CharField(max_length=255, null=True, blank=True)
    transportation = models.CharField(max_length=255, null=True, blank=True)
    other_benefits = models.TextField(null=True, blank=True)
    
    # Working conditions
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    overtime_allowed = models.BooleanField(default=True)
    contract_period_months = models.IntegerField(null=True, blank=True)
    
    # Visa information
    visa_type = models.CharField(max_length=100, null=True, blank=True)
    visa_sponsor = models.CharField(max_length=255, null=True, blank=True)
    
    # Timeline
    posting_date = models.DateField(auto_now_add=True)
    application_deadline = models.DateField()
    interview_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    is_active = models.BooleanField(default=True)
    
    # Metadata
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='jobs_created')
    
    class Meta:
        ordering = ['-posting_date']
        indexes = [
            models.Index(fields=['country', 'status']),
            models.Index(fields=['employer', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.country} ({self.job_id})"
    
    @property
    def available_positions(self):
        """Calculate remaining open positions"""
        return max(0, self.quantity - self.filled_count)


class Employer(models.Model):
    """Employer/Client model"""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    employer_id = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255, unique=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100)
    
    # Business details
    license = models.CharField(max_length=100, null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Payment terms
    payment_terms = models.CharField(max_length=100, default='NET-30')
    currency = models.CharField(max_length=3, default='USD')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['company_name']
    
    def __str__(self):
        return self.company_name