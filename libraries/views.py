from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse, FileResponse, HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from libraries.forms import DocumentTypeForm, CategoryTypeForm, SectionTypeForm, DivisionTypeForm
from libraries.models import DocumentType,CategoryType, DivisionType, SectionType
import os

# Create your views here.

@login_required
def category_type_page(request, action=None, pk=None):
    try:
        page_num = 1 if not request.GET.get('page') else request.GET.get('page')
        context = {
            'module_name': 'Category Type',
            'title': 'Records | Libraries - Category Type',
            'action': action,
            'breadcrumbs': None,
            'form' : CategoryTypeForm()
        }
        if action is None and pk is None:
            if request.method == "POST":
                with transaction.atomic():
                    form = CategoryTypeForm(request.POST)
                    if form.is_valid():
                        name = form.clean_categorytype()
                        is_active = form.cleaned_data['is_active']
                        f = CategoryType.objects.create(name=name, is_active=is_active, created_by=request.user)
                        return JsonResponse({'statusMsg': 'Success'}, status=200)
                    return JsonResponse({'statusMsg': form.errors}, status=404)

        if action is not None and pk is None:
            if action == "filter":
                if request.method == "GET":
                    keyword = request.GET.get('keyword')
                    context['data'] = Paginator(CategoryType.objects.filter(Q(name__icontains=keyword)).order_by('-date_created'), 10).page(page_num)
                    context['keyword'] = keyword
                    return render(request, 'libraries/category_type/partial_category_type.html', context)
        
        if action == "delete" and pk is not None:
            if request.method == "POST":
                categorytype =CategoryType.objects.filter(id=pk).first()
                if categorytype:
                    categorytype.delete()
                return JsonResponse({'statusMsg': 'category deleted successfully'}, status=200)

        if action is not None and pk is not None:
            categorytype = CategoryType.objects.get(id=pk)
            if action == "update":
                if request.method == "POST":
                    form = CategoryTypeForm(request.POST, instance=categorytype)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                context['form'] = CategoryTypeForm(instance=categorytype)
                context['data'] = categorytype 
                return render(request, 'libraries/category_type/update_category_type.html', context)

        context['data'] = Paginator(CategoryType.objects.order_by('-date_created'), 10).page(page_num)

        template = 'libraries/category_type/index.html' if not request.GET.get('page') else \
            'libraries/category_type/partial_category_type.html'

        return render(request, template, context)

    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)    


 #Libraries       
@login_required
def document_type_page(request, action=None, pk=None):
    try:
        page_num = 1 if not request.GET.get('page') else request.GET.get('page')
        context = {
            'module_name': 'Document Type',
            'title': 'Records | Libraries - Document Type',
            'action': action,
            'breadcrumbs': None,
            'form' : DocumentTypeForm()
        }
        if action is None and pk is None:
            if request.method == "POST":
                with transaction.atomic():
                    form = DocumentTypeForm(request.POST)
                    if form.is_valid():
                        name = form.clean_documenttype()
                        is_active = form.cleaned_data['is_active']
                        f = DocumentType.objects.create(name=name, is_active=is_active, created_by=request.user)
                        return JsonResponse({'statusMsg': 'Success'}, status=200)
                    return JsonResponse({'statusMsg': form.errors}, status=404)

        if action is not None and pk is None:
            if action == "filter":
                if request.method == "GET":
                    keyword = request.GET.get('keyword')
                    context['data'] = Paginator(DocumentType.objects.filter(Q(name__icontains=keyword)).order_by('-date_created'), 10).page(page_num)
                    context['keyword'] = keyword
                    return render(request, 'libraries/document_type/partial_document_type.html', context)
        
        if action == "delete" and pk is not None:
            if request.method == "POST":
                documenttype =DocumentType.objects.filter(id=pk).first()
                if documenttype:
                    documenttype.delete()
                return JsonResponse({'statusMsg': 'File deleted successfully'}, status=200)

        if action is not None and pk is not None:
            documenttype = DocumentType.objects.get(id=pk)
            if action == "update":
                if request.method == "POST":
                    form = DocumentTypeForm(request.POST, instance=documenttype)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                context['form'] = DocumentTypeForm(instance=documenttype)
                context['data'] = documenttype 
                return render(request, 'libraries/document_type/update_document_type.html', context)
            
    

        context['data'] = Paginator(DocumentType.objects.order_by('-date_created'), 10).page(page_num)

        template = 'libraries/document_type/index.html' if not request.GET.get('page') else \
            'libraries/document_type/partial_document_type.html'

        return render(request, template, context)

    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)
    

@login_required
def division_type_page(request, action=None, pk=None):
    try:
        page_num = 1 if not request.GET.get('page') else request.GET.get('page')
        context = {
            'module_name': 'Division Type',
            'title': 'Records | Libraries - Division Type',
            'action': action,
            'breadcrumbs': None,
            'form' : DivisionTypeForm()
        }
        if action is None and pk is None:
            if request.method == "POST":
                with transaction.atomic():
                    form = DivisionTypeForm(request.POST)
                    if form.is_valid():
                        name = form.clean_divisiontype()
                        is_active = form.cleaned_data['is_active']
                        f = DivisionType.objects.create(name=name, is_active=is_active, created_by=request.user)
                        return JsonResponse({'statusMsg': 'Success'}, status=200)
                    return JsonResponse({'statusMsg': form.errors}, status=404)

        if action is not None and pk is None:
            if action == "filter":
                if request.method == "GET":
                    keyword = request.GET.get('keyword')
                    context['data'] = Paginator(DivisionType.objects.filter(Q(name__icontains=keyword)).order_by('-date_created'), 10).page(page_num)
                    context['keyword'] = keyword
                    return render(request, 'libraries/division_type/partial_division_type.html', context)
        
        if action == "delete" and pk is not None:
            if request.method == "POST":
                divisiontype =DivisionType.objects.filter(id=pk).first()
                if divisiontype:
                    divisiontype.delete()
                return JsonResponse({'statusMsg': 'File deleted successfully'}, status=200)

        if action is not None and pk is not None:
            divisiontype = DivisionType.objects.get(id=pk)
            if action == "update":
                if request.method == "POST":
                    form = DivisionTypeForm(request.POST, instance=divisiontype)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                context['form'] = DivisionTypeForm(instance=divisiontype)
                context['data'] = divisiontype 
                return render(request, 'libraries/division_type/update_division_type.html', context)
            
    

        context['data'] = Paginator(DivisionType.objects.order_by('-date_created'), 10).page(page_num)

        template = 'libraries/division_type/index.html' if not request.GET.get('page') else \
            'libraries/division_type/partial_division_type.html'

        return render(request, template, context)

    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)
    
@login_required
def section_type_page(request, action=None, pk=None):
    try:
        page_num = 1 if not request.GET.get('page') else request.GET.get('page')
        context = {
            'module_name': 'Section Type',
            'title': 'Records | Libraries - Section Type',
            'action': action,
            'breadcrumbs': None,
            'form' : SectionTypeForm()
        }
        if action is None and pk is None:
            if request.method == "POST":
                with transaction.atomic():
                    form = SectionTypeForm(request.POST)
                    if form.is_valid():
                        name = form.clean_sectiontype()
                        is_active = form.cleaned_data['is_active']
                        f = SectionType.objects.create(name=name, is_active=is_active, created_by=request.user)
                        return JsonResponse({'statusMsg': 'Success'}, status=200)
                    return JsonResponse({'statusMsg': form.errors}, status=404)

        if action is not None and pk is None:
            if action == "filter":
                if request.method == "GET":
                    keyword = request.GET.get('keyword')
                    context['data'] = Paginator(SectionType.objects.filter(Q(name__icontains=keyword)).order_by('-date_created'), 10).page(page_num)
                    context['keyword'] = keyword
                    return render(request, 'libraries/section_type/partial_section_type.html', context)
        
        if action == "delete" and pk is not None:
            if request.method == "POST":
                sectiontype =SectionType.objects.filter(id=pk).first()
                if sectiontype:
                    sectiontype.delete()
                return JsonResponse({'statusMsg': 'File deleted successfully'}, status=200)

        if action is not None and pk is not None:
            sectiontype = SectionType.objects.get(id=pk)
            if action == "update":
                if request.method == "POST":
                    form = SectionTypeForm(request.POST, instance=sectiontype)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                context['form'] = SectionTypeForm(instance=sectiontype)
                context['data'] = sectiontype 
                return render(request, 'libraries/section_type/update_section_type.html', context)
            
    

        context['data'] = Paginator(SectionType.objects.order_by('-date_created'), 10).page(page_num)

        template = 'libraries/section_type/index.html' if not request.GET.get('page') else \
            'libraries/section_type/partial_section_type.html'

        return render(request, template, context)

    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)
    