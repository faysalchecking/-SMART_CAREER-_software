from django.db import models
from django.utils import timezone

class DocumentType(models.Model):
    """Document type configuration"""
    
    TYPE_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('NID', 'National ID'),
        ('PHOTO', 'Photo'),
        ('CV', 'CV'),
        ('BIRTH_CERT', 'Birth Certificate'),
        ('EDU_CERT', 'Educational Certificate'),
        ('EXP_CERT', 'Experience Certificate'),
        ('POLICE_CLEAR', 'Police Clearance'),
        ('MEDICAL_CERT', 'Medical Certificate'),
        ('TRAINING_CERT', 'Training Certificate'),
        ('CONTRACT', 'Contract'),
        ('VISA', 'Visa'),
        ('EMBASSY_DOC', 'Embassy Document'),
        ('CLEARANCE', 'Clearance'),
        ('TICKET', 'Ticket'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True, choices=TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    is_required = models.BooleanField(default=False)
    expirable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Document(models.Model):
    """Candidate document"""
    
    STATUS_CHOICES = [
        ('UPLOADED', 'Uploaded'),
        ('PENDING_VERIFICATION', 'Pending Verification'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired'),
        ('SUPERSEDED', 'Superseded'),
    ]
    
    QUALITY_CHOICES = [
        ('CLEAR', 'Clear'),
        ('ACCEPTABLE', 'Acceptable'),
        ('POOR', 'Poor Quality'),
    ]
    
    # Relationships
    candidate = models.ForeignKey('candidates.Candidate', on_delete=models.CASCADE, related_name='documents')
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    
    # File information
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # in bytes
    mime_type = models.CharField(max_length=100)
    
    # Document details
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    document_number = models.CharField(max_length=100, null=True, blank=True)
    
    # Verification
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPLOADED')
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents_verified')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(null=True, blank=True)
    
    # Quality
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, null=True, blank=True)
    
    # Metadata
    version = models.IntegerField(default=1)
    is_original = models.BooleanField(default=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='documents_uploaded')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['candidate', 'document_type']),
            models.Index(fields=['status']),
            models.Index(fields=['expiry_date']),
        ]
    
    def __str__(self):
        return f"{self.candidate.full_name} - {self.document_type.name}"
    
    @property
    def is_expired(self):
        """Check if document is expired"""
        if not self.expiry_date:
            return False
        from datetime import date
        return self.expiry_date < date.today()
    
    @property
    def days_until_expiry(self):
        """Days remaining until expiry"""
        if not self.expiry_date:
            return None
        from datetime import date
        delta = self.expiry_date - date.today()
        return delta.days


class PassportScan(models.Model):
    """Passport scan and OCR data"""
    
    STATUS_CHOICES = [
        ('NEW', 'New Scan'),
        ('PROCESSING', 'Processing'),
        ('EXTRACTED', 'Extracted'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]
    
    # Relationships
    candidate = models.OneToOneField('candidates.Candidate', on_delete=models.CASCADE, related_name='passport_scan')
    document = models.OneToOneField(Document, on_delete=models.CASCADE, null=True, blank=True, related_name='passport_scan')
    
    # OCR Results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    
    # Extracted data
    mrz_data = models.TextField(null=True, blank=True)  # Machine Readable Zone raw
    passport_number = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    given_name = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issuing_country = models.CharField(max_length=100, null=True, blank=True)
    
    # Confidence scores
    passport_number_confidence = models.FloatField(default=0)
    surname_confidence = models.FloatField(default=0)
    given_name_confidence = models.FloatField(default=0)
    date_of_birth_confidence = models.FloatField(default=0)
    expiry_date_confidence = models.FloatField(default=0)
    
    # Validation
    mrz_valid = models.BooleanField(default=False)
    all_fields_confident = models.BooleanField(default=False)
    
    # Human verification
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Passport Scan - {self.candidate.full_name}"
    
    @property
    def requires_verification(self):
        """Check if needs human verification"""
        return not self.all_fields_confident or not self.mrz_valid