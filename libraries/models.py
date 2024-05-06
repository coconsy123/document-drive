from django.db import models
import uuid
from frontend.models import Account
from django.apps import apps
# Create your models here.


class CategoryType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(Account, models.RESTRICT, related_name="category_type_created_by")
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="category_type_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'tbl_categorytype'

class DocumentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(Account, models.RESTRICT, related_name="document_type_created_by")
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="document_type_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'tbl_documenttype'

class SectionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #division_type = models.ForeignKey('DivisionType', models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(Account, models.RESTRICT, related_name="section_type_created_by")
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="section_type_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'tbl_sectiontype'

class DivisionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(Account, models.RESTRICT, related_name="division_type_created_by")
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="division_type_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'tbl_divisiontype'



class CaseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(Account, models.RESTRICT, related_name="case_category_created_by")
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Account, models.RESTRICT, related_name="case_category_updated_by", null=True)
    date_updated = models.DateTimeField(auto_now_add=False, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'tbl_casecategory'

