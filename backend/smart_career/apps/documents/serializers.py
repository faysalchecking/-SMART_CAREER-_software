from rest_framework import serializers
from .models import Document, DocumentType, PassportScan

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description', 'is_required', 'expirable']

class DocumentSerializer(serializers.ModelSerializer):
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    is_expired = serializers.ReadOnlyField()
    days_until_expiry = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'candidate', 'document_type', 'document_type_name', 'file',
            'original_filename', 'issue_date', 'expiry_date', 'status',
            'verified_at', 'verification_notes', 'is_expired', 'days_until_expiry',
            'quality', 'remarks', 'uploaded_at'
        ]
        read_only_fields = ['id', 'file', 'is_expired', 'days_until_expiry', 'uploaded_at']

class PassportScanSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.full_name', read_only=True)
    requires_verification = serializers.ReadOnlyField()
    
    class Meta:
        model = PassportScan
        fields = [
            'id', 'candidate', 'candidate_name', 'status', 'passport_number',
            'surname', 'given_name', 'nationality', 'date_of_birth', 'gender',
            'issue_date', 'expiry_date', 'issuing_country',
            'passport_number_confidence', 'date_of_birth_confidence',
            'expiry_date_confidence', 'mrz_valid', 'all_fields_confident',
            'requires_verification', 'verified_at', 'verification_notes',
            'created_at'
        ]
        read_only_fields = ['id', 'requires_verification', 'created_at']

class PassportUploadSerializer(serializers.Serializer):
    """For passport image upload"""
    candidate = serializers.IntegerField()
    image = serializers.ImageField()
    
    def validate_image(self, value):
        # Check file size (max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be less than 5MB")
        return value