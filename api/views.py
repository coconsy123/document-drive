from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from backend.models import ContractFiles
from api.serializers import ContractFilesSerializer



class ContractFilesViews(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractFilesSerializer

    def get_queryset(self):
        queryset = ContractFiles.objects.all()
        category_id = self.request.query_params.get('category_id')
        division_id = self.request.query_params.get('division_id')
        section_id = self.request.query_params.get('section_id')
        if category_id:
            queryset = queryset.filter(category_type__id=category_id)
        if division_id:
            queryset = queryset.filter(division_type__id=division_id)
        if section_id:
            queryset = queryset.filter(section_type__id=section_id)
        return queryset.order_by('-id')
    
    
