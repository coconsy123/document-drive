from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from backend.views import accounts_page, contract_files_dashboard, system_logs, contract_files_page, case_files_page, contract_files_reports, print



urlpatterns = [

    path('accounts/', accounts_page, name='backend-accounts-page'),
    path('accounts/<slug:action>/', accounts_page, name='backend-accounts-page'),
    path('accounts/<slug:action>/<slug:pk>/', accounts_page, name='backend-accounts-page'),

    path('dashboard/', contract_files_dashboard, name='backend-dashboard-page'),
    path('dashboard/<slug:action>', contract_files_dashboard, name='backend-dashboard-page'),
    path('dashboard/<slug:action>/<slug:pk>', contract_files_dashboard, name='backend-dashboard-page'),

    path('contract_files/', contract_files_page, name='backend-contract-files-page'),
    path('pdf-viewer/', contract_files_page, name='pdf-viewer'),
    path('contract_files/<slug:action>', contract_files_page, name='backend-contract-files-page'),
    path('contract_files/<slug:action>/<slug:pk>', contract_files_page, name='backend-contract-files-page'),

    path('case_files/', case_files_page, name='backend-case-files-page'),
    path('case_files/<slug:action>', case_files_page, name='backend-case-files-page'),
    path('case_files/<slug:action>/<slug:pk>', case_files_page, name='backend-case-files-page'),

    path('reports/', contract_files_reports, name='backend-generate-report'),
    path('reports/<slug:action>', contract_files_reports, name='backend-generate-report'),
    path('reports/<slug:action>/<slug:pk>', contract_files_reports, name='backend-generate-report'),
    path('print_report/', print, name='print-report'),

    path('system_logs/', system_logs, name='backend-system-logs-page'),
    path('system_logs/<slug:action>', system_logs, name='backend-system-logs-page'),
    path('system_logs/<slug:action>/<slug:pk>', system_logs, name='backend-system-logs-page'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)