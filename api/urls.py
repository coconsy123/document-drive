
from django.urls import path

from api.views import ContractFilesViews,PDFFileListView

urlpatterns = [
    path('contract_files/', ContractFilesViews.as_view(), name='api-contract-files'),
    path('pdf-files/', PDFFileListView.as_view(), name='pdf-file-list'),
]
