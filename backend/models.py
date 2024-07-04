from django.db import models
import uuid
from frontend.models import Account
from django.apps import apps
from libraries.models import *
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class CaseFiles(models.Model):
    CASE_STATUS_CHOICES = [
        ('Sample1', 'Sample1'),
        ('Sample2', 'Sample2'),
        ('Sample3', 'Sample3'),
        ('Sample4', 'Sample4'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    date_case_filed = models.DateTimeField(null=True, blank=True)
    date_case_received = models.DateTimeField(null=True, blank=True)
    case_category = models.ForeignKey(CaseCategory, models.SET_NULL, null=True)
    case_nature = models.ForeignKey(CaseNature, models.SET_NULL, null=True)
    case_status = models.CharField(max_length=255, choices=CASE_STATUS_CHOICES)
    others = models.TextField()
    amount = models.FloatField()
    others = models.CharField(max_length=255)
    date_returned = models.DateTimeField(null=True, blank=True)
    date_removed = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=255)
    details = models.TextField()
    
    
class ContractFiles(models.Model):
    FILE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Completed', 'Completed'),
        ('Archived', 'Archived'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    division_type = models.ForeignKey(DivisionType, models.SET_NULL, null=True)
    section_type = models.ForeignKey(SectionType, models.SET_NULL, null=True)
    category_type = models.ForeignKey(CategoryType, models.SET_NULL, null=True)
    created_by = models.ForeignKey(Account, models.RESTRICT, related_name="file_upload_created_by")
    status = models.CharField(max_length=255, choices=FILE_STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="file_upload_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    begin_date_completed = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField()
    date_of_coverage = models.CharField(max_length=255)
    
    def is_archivable(self):
        """Check if 1 minute has passed since the file was completed."""
        if self.status != "Completed" or not self.begin_date_completed:
            return False
        return timezone.now() > self.begin_date_completed + timedelta(days=180)
    
    def time_until_archivable(self):
        """Calculate the remaining time until the file can be archived."""
        if self.status != "Completed" or not self.begin_date_completed:
            return None
        time_passed = timezone.now() - self.begin_date_completed
        if time_passed < timedelta(days=180):
            # Calculate the remaining time
            remaining_time = timedelta(days=180) - time_passed
            return remaining_time
        return None
    
    def full_name(self):
        return self.created_by.firstname and self.created_by.lastname if self.created_by else None
        
    def division_type_name(self):
         return self.division_type.name if self.division_type else None

    def category_type_name(self):
         return self.category_type.name if self.category_type else None
    
    def document_type(self):
        return AdditionalFile.objects.filter(contract_files_id=self.id).order_by('-date_created')
   
    
    def document_type_name(self):
        additional_file = AdditionalFile.objects.filter(contract_files_id=self.id).order_by('-date_created').first()
        return additional_file.document_type.name if additional_file else None
    
    def status_color(self):
        if self.status == "Pending":
            return f'<span class="badge badge-primary">{self.status.upper()}</span>'
        elif self.status == "Reviewed":
            return f'<span class="badge badge-danger">{self.status.upper()}</span>'
        elif self.status == "Completed":
            return f'<span class="badge badge-success">{self.status.upper()}</span>'
        elif self.status == "Archived":
            return f'<span class="badge badge-warning">{self.status.upper()}</span>'
       
    def __str__(self):
        return self.title
    
    class Meta:
        managed = False
        db_table = 'tbl_contractfiles'

class AdditionalFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contract_files = models.ForeignKey(ContractFiles, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, models.RESTRICT)
    file_directory = models.CharField(max_length=255)
    created_by = models.ForeignKey(Account, models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="addtionalfile_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'tbl_additionalfile'

class FileUpdate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    remarks = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account, models.RESTRICT)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)


    class Meta:
        managed = False
        db_table = 'tbl_fileupdate'


class ContractReport(models.Model):
    CONTRACT_REPORT = [
        ('New', 'New'),
        ('Amendment', 'Amendment'),
        ('Renewal', 'Renewal'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact_no = models.CharField(max_length=255, null=False, blank=True)
    title = models.CharField(max_length=255)
    date_of_contract = models.DateField(auto_now_add=False, null=True)
    proponents_obsu = models.CharField(max_length=255, null=False, blank=True)
    type_of_contract = models.CharField(max_length=255, choices=CONTRACT_REPORT)
    date_of_coverage = models.DateField(auto_now_add=False, null=False)
    remarks = models.CharField(max_length=255, null=False, blank=True)


    class Meta:
        managed = False
        db_table = 'tbl_contractreport'

