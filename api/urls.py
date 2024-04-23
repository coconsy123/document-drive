
from django.urls import path

from api.views import ContractFilesViews

urlpatterns = [
    path('contract_files/', ContractFilesViews.as_view(), name='api-contract-files'),
]
