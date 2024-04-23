from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse, FileResponse, HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from frontend.models import Account
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from libraries.models import DocumentType,  CategoryType, DivisionType
from backend.models import ContractFiles, FileUpdate, AdditionalFile
import os
import urllib.parse

@login_required
def contract_files_dashboard(request, action=None, pk=None):
    context = {
        'module_name': 'Dashboard',
        'title': 'Records | Backend - Dashboard',
        'action': action,
        'breadcrumbs': None,
        'form': None,

    }
    page_num = 1 if not request.GET.get('page') else request.GET.get('page')
    if action is not None and pk is None:
        if action == "filter":
            if request.method == "GET":
                keyword = request.GET.get('keyword')
                context['data'] = Paginator(FileUpdate.objects.filter(Q(title__icontains=keyword)).order_by('-date_created'), 5).page(page_num)
                context['keyword'] = keyword
                return render(request, 'backend/contract_files/dashboard/partial-dashboard.html', context)
            
    context['data'] = FileUpdate.objects.all()
    context['data'] = Paginator(FileUpdate.objects.order_by('-date_created'), 5).page(page_num)

    template = 'backend/contract_files/dashboard/dashboard.html' if not request.GET.get('page') else \
    'backend/contract_files/dashboard/partial-dashboard.html'
    return render(request, template, context)
    



@login_required
def contract_files_page(request, action=None, pk=None):
    context = {
        'module_name': 'Contract Files',
        'title': 'Records | Backend - Contract Files',
        'action': action,
        'breadcrumbs': ['Contract Files'],
        'form': None,
        'keyword': None,
    }
    page_num = 1 if not request.GET.get('page') else request.GET.get('page')
    if action is not None and pk is None:
        if action == "add" and request.method == "GET":
            context['breadcrumbs'].append('Add')
            return render(request, 'backend/contract_files/add-files.html', context)
             
        elif action == "add" and request.method == "POST":
            with transaction.atomic():
                title = request.POST.get('title')
                t = ContractFiles.objects.filter(title=title).first()
                if t:
                    return JsonResponse({'statusMsg': 'Already exist!'}, status=404)
                else:
                    description = request.POST.get('description')
                    category_type_id = request.POST.get('category_type')
                    division_type_id = request.POST.get('division_type')
                    category_type = CategoryType.objects.filter(id=category_type_id).first()
                    division_type = DivisionType.objects.filter(id=division_type_id).first()
                    document_type = request.POST.getlist('document_type')
                    remarks = request.POST.get('remarks')
                    documents = request.FILES.getlist('documents')
                    document_type_data = [
                        {
                            'document_type_id': dti,
                            'document': d
                        }
                        for dti, d in zip(document_type, documents)
                    ]

                    contract_files = ContractFiles.objects.create(title=title,description=description,category_type=category_type,division_type=division_type,created_by=request.user, remarks=remarks, status="Pending")

                    for row in document_type_data:
                        fs = FileSystemStorage()
                        name = fs.save(row['document'].name, row['document'])
                        additional_file = AdditionalFile.objects.create(document_type_id=row['document_type_id'],
                                                                        contract_files=contract_files,
                                                                        file_directory=fs.url(name),
                                                                        created_by=request.user)
                        file_update = FileUpdate.objects.create(title=f"{contract_files.title}", remarks="file has been added by", created_by=request.user)
                        
                    context['breadcrumbs'].append('Add')
                    return JsonResponse({'statusMsg': 'Success'}, status=200)
             
        elif action == "add-document":
            if request.method == "GET":
                return render(request, 'backend/contract_files/add-document.html', context)
            
        elif action == "searching":
            if request.method == "GET":
                keyword = request.GET.get('keyword')
                context['data'] = Paginator(ContractFiles.objects.filter(Q(title__icontains=keyword)).order_by('-date_created'), 12).page(page_num)
                context['keyword'] = keyword
                return render(request, 'backend/contract_files/partial-file-upload.html', context)
            
        
        elif action == "filter":
            if request.method == "GET":
                category_type_id = request.GET.get('category_type') if request.GET.get('category_type') != "None" else None
                division_type_id = request.GET.get('division_type') if request.GET.get('division_type') != "None" else None
                status = request.GET.get('status') if request.GET.get('status') != "None" and request.GET.get('status') != "" else None

                queryset = ContractFiles.objects.filter(is_active=True)

                if category_type_id:
                    queryset = queryset.filter(category_type_id=category_type_id)

                if division_type_id:
                    queryset = queryset.filter(division_type_id=division_type_id)

                if status:
                    queryset = queryset.filter(status=status)
                

                context['data'] = Paginator(queryset.order_by('-date_created'), 12).page(page_num)

                keyword = []
                if category_type_id:
                    keyword.append(f"category_type={category_type_id}")
                if division_type_id:
                    keyword.append(f"division_type={division_type_id}")
                if status:
                    keyword.append(f"status={status}")
                context['keyword'] = "&".join(keyword)
                return render(request, 'backend/contract_files/partial-file-upload.html', context)
                
    elif action is not None and pk is not None:
        contract_files = ContractFiles.objects.get(id=pk)
        context['data'] = contract_files 
        if action == "view" and request.method == "GET":
            context['breadcrumbs'] = ['Contract File', str(contract_files.id)]
            return render(request, 'backend/contract_files/update-files.html', context)

        elif action == "add-additional-file" and contract_files.created_by == request.user:
            if request.method == "POST":
                document_type_id = request.POST.get('document_type_id')
                title = request.POST.get('title')
                description = request.POST.get('description')
                fs = FileSystemStorage()
                name = fs.save(request.FILES.get('document').name, request.FILES.get('document'))
                additional_file = AdditionalFile.objects.create(document_type_id=document_type_id,
                                                                            contract_files=contract_files,
                                                                            file_directory=fs.url(name),
                                                                            created_by=request.user)
                file_update = FileUpdate.objects.create(title=f"{name}", remarks="document has been added by", created_by=request.user)
                if additional_file:
                        return JsonResponse({'statusMsg': 'Success'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Something went wrong!'}, status=404)
        
                
        elif action == "update-file" and request.method == "POST" and contract_files.created_by == request.user:
            try:
                title = request.POST.get('title')
                description = request.POST.get('description')
                remarks = request.POST.get('remarks')
                category_type_id = request.POST.get('category_type_id')
                division_type_id = request.POST.get('division_type_id')
                
                category_type = CategoryType.objects.filter(id=category_type_id).first()
                division_type = DivisionType.objects.filter(id=division_type_id).first()

                contract_files.title = title
                contract_files.description = description
                contract_files.remarks = remarks
                contract_files.category_type = category_type
                contract_files.division_type = division_type
                contract_files.date_updated = timezone.now()
                contract_files.updated_by = request.user
                contract_files.save()
                file_update = FileUpdate.objects.create(title=f"{contract_files.title}", remarks="file has been updated by", created_by=request.user)

                return JsonResponse({'statusMsg': 'Success'}, status=200)
            except Exception as e: 
                    return JsonResponse({'statusMsg': 'File not found'}, status=404)
            
            
        elif action == "delete-additional-file" in request.path and request.method == "POST" and contract_files.created_by == request.user:
            additional_file_id = request.POST.get('additional_file_id')
            additional_file = AdditionalFile.objects.filter(id=additional_file_id).first()

            if additional_file:
                file_path = additional_file.file_directory
                file_name = os.path.basename(file_path)

                file_path = urllib.parse.unquote(file_path)

                # Correctly building the file system path
                if file_path.startswith(settings.MEDIA_URL):
                    file_system_path = os.path.join(settings.MEDIA_ROOT, file_path[len(settings.MEDIA_URL):])
                    if os.path.exists(file_system_path):
                        os.remove(file_system_path)
                        directory = os.path.dirname(file_system_path)
                        if not os.listdir(directory):  # Check if directory is empty
                            os.rmdir(directory)

                additional_file.delete()
                FileUpdate.objects.create(title=file_name, remarks="file has been deleted by", created_by=request.user)
                return JsonResponse({'statusMsg': 'Success'}, status=200)
            else:
                return JsonResponse({'statusMsg': 'Additional file not found'}, status=404)

             
        elif action == "update-additional-file" and request.method == "POST" and contract_files.created_by == request.user:
            try:
                file_directory = None
                additional_file = None
                if request.FILES.get('document'):
                    fs = FileSystemStorage()
                    name = fs.save(request.FILES.get('document').name, request.FILES.get('document'))
                    file_directory = fs.url(name)
                    additional_file = AdditionalFile.objects.filter(
                        id=request.method.get('additional_file_id')).update(
                        document_type_id=request.POST.get('document_type_id'), file_directory=file_directory)
                else:
                    additional_file = AdditionalFile.objects.filter(id=request.POST.get('additional_file_id')).update(document_type_id=request.POST.get('document_type_id'))

                
                if additional_file is not None and additional_file > 0:
                    return JsonResponse({'statusMsg': 'Attachment Successfully Updated!', 'file_directory': file_directory}, status=200)
                
                else:
                    return JsonResponse({'statusMsg': 'Something went wrong!'}, status=404)
                
            except Exception as e:
                return JsonResponse({'statusMsg': str(e)}, status=404)
            
        elif action == "file-reviewed":
            contract_files.status = "Reviewed"
            contract_files.save()
            file_update = FileUpdate.objects.create(title=f"{contract_files.title}", remarks=f"file has been {contract_files.status} by", created_by=request.user)
            return JsonResponse({'statusMsg': 'Success'}, status=200)

        elif action == "file-completed":
            completion_date = request.POST.get('begin_date_completed')
            contract_files.status = "Completed"
            contract_files.begin_date_completed = timezone.make_aware(datetime.strptime(completion_date, '%Y-%m-%d'))
            contract_files.save()
            file_update = FileUpdate.objects.create(title=f"{contract_files.title}", remarks=f"file has been {contract_files.status} by", created_by=request.user)
            return JsonResponse({'statusMsg': 'Success'}, status=200)
        
        elif action == "file-archived":
            contract_files.status = "Archived"
            contract_files.save()
            file_update = FileUpdate.objects.create(title=f"{contract_files.title}", remarks=f"file has been {contract_files.status} by", created_by=request.user)
            return JsonResponse({'statusMsg': 'Success'}, status=200)
        else:
            return JsonResponse({'statusMsg': 'Unauthorized Access!'}, status=404)
        

    context['status'] = ['Pending', 'Reviewed', 'Completed', 'Archived']
    context['data'] = ContractFiles.objects.all()
    context['data'] = Paginator(ContractFiles.objects.order_by('-date_created'), 12).page(page_num)

    template = 'backend/contract_files/files.html' if not request.GET.get('page') else \
    'backend/contract_files/partial-file-upload.html'
    return render(request, template, context)

def contract_files_reports(request,action=None, pk=None):
    context = {
        'module_name': 'Generate Report',
        'title': 'Records | Backend - Generate Report',
        'action': action,
        'breadcrumbs': ['Generate Report'],
        'form': None,
        'keyword': None,
    }

    return render(request, 'backend/contract_files/reports/reports.html', context )

def print(request):
    return render(request, 'backend/contract_files/reports/print_report.html' )



def case_files_page(request, action=None, pk=None):
    context = {
        'module_name': 'Case Files',
        'title': 'Records | Backend - Case Files',
        'action': action,
        'breadcrumbs': ['Case Files'],
        'form': None,
    }
    return render(request, 'backend/case_files/add-case-files.html')

@login_required
def system_logs(request, action=None, pk=None):
     context = {
        'module_name': 'System Logs',
        'title': 'Records | Backend - System Logs',
        'action': action,
        'breadcrumbs': ['System Logs'],
        'form': None,
     }
     page_num = 1 if not request.GET.get('page') else request.GET.get('page')
     if action is not None and pk is None:
        if action == "filter":
            if request.method == "GET":
                keyword = request.GET.get('keyword')
                context['data'] = Paginator(FileUpdate.objects.filter(Q(title__icontains=keyword)).order_by('-date_created'), 5).page(page_num)
                context['keyword'] = keyword
                return render(request, 'backend/system_logs/partial-system-logs.html', context)
            
     context['data'] = FileUpdate.objects.all()
     context['data'] = Paginator(FileUpdate.objects.order_by('-date_created'), 5).page(page_num)

     template = 'backend/system_logs/system-logs.html' if not request.GET.get('page') else \
     'backend/system_logs/partial-system-logs.html'
     return render(request, template, context)
