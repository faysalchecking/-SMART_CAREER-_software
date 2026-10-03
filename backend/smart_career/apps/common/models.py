from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    """Audit trail for all important actions"""
    
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
        ('DOWNLOAD', 'Download'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=255)
    resource_id = models.IntegerField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'common_audit_log'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['resource', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.resource}"