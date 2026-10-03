from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile for SMART CAREER"""
    
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('recruitment_manager', 'Recruitment Manager'),
        ('recruiter', 'Recruiter'),
        ('data_entry', 'Data Entry Operator'),
        ('medical_officer', 'Medical Officer'),
        ('visa_officer', 'Visa Officer'),
        ('finance_officer', 'Finance Officer'),
        ('agent', 'Agent'),
        ('client', 'Client/Employer'),
        ('candidate', 'Candidate'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'authentication_user_profile'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"