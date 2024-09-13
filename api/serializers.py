from rest_framework import serializers
from backend.models import ContractFiles, AdditionalFile, DocumentType  # Ensure all needed models are imported

class ContractFilesSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    date_updated = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    division_type_name = serializers.CharField(source="division_type", read_only=True)
    section_type_name = serializers.CharField(source="section_type", read_only=True)
    category_type_name = serializers.CharField(source="category_type", read_only=True)
    full_name = serializers.CharField(source="created_by", read_only=True)
    status_color = serializers.CharField(read_only=True, default=None)
    
    file_directories = serializers.SerializerMethodField()
    
    class Meta:
        model = ContractFiles
        fields = '__all__'
        
    def get_file_directories(self, obj):
        """Retrieve the file_directory of all related AdditionalFile objects for this ContractFiles instance."""
        additional_files = AdditionalFile.objects.filter(contract_files=obj, is_active=True)
        # Return a list of file_directory values or filter to only return PDFs
        return [file.file_directory for file in additional_files if file.file_directory.lower().endswith('.pdf')]
        
class AdditionalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalFile
        fields = ['id', 'title', 'description', 'file_directory', 'date_created', 'is_active']
        
    def validate_file_directory(self, value):
        if not value.lower().endswith('.pdf'):
            raise serializers.ValidationError("File must be a PDF.")
        return value