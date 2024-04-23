from rest_framework import serializers
from backend.models import ContractFiles, DocumentType  # Ensure all needed models are imported

class ContractFilesSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    date_updated = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    division_type_name = serializers.CharField(source="division_type", read_only=True)
    category_type_name = serializers.CharField(source="category_type", read_only=True)
    full_name = serializers.CharField(source="created_by", read_only=True)
    status_color = serializers.CharField(read_only=True, default=None)
    
    class Meta:
        model = ContractFiles
        fields = '__all__'


        
