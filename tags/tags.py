from django import template
from datetime import datetime
from django.utils.safestring import mark_safe
from backend.models import *
from libraries.models import *
from frontend.models import Account
import json
from datetime import timedelta


register = template.Library()
'''
@register.filter(name='format_timedelta')
def format_timedelta(value):
    if not value or not isinstance(value, timedelta):
        return ""
    # Convert timedelta to total seconds
    total_seconds = int(value.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes} minutes, {seconds} seconds"
'''

@register.filter(name='format_timedelta')
def format_timedelta(value):
    if not value or not isinstance(value, timedelta):
        return ""
    # Extract days, seconds from timedelta
    days = value.days
    seconds_remainder = value.seconds
    hours = seconds_remainder // 3600
    minutes = (seconds_remainder % 3600) // 60

    # Formatting output
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    else:
        return f"{minutes} minutes"

@register.simple_tag
def document_type():
    return DocumentType.objects.order_by('-date_created')

@register.simple_tag
def category_type():
    return CategoryType.objects.order_by('-date_created')

@register.simple_tag
def division_type():
    return DivisionType.objects.order_by('-date_created')

@register.simple_tag
def section_type():
    return SectionType.objects.order_by('-date_created')

@register.simple_tag
def to_str(data):
    return str(data)

@register.simple_tag
def get_file_upload_count(status=None):
    if status:
        if status == "Pending":
            return ContractFiles.objects.filter(status=status).count()
        elif status == "Reviewed":
            return ContractFiles.objects.exclude(status="Pending").exclude(status="Completed").exclude(status="Archived").count()
        elif status == "Completed":
            return ContractFiles.objects.filter(status=status).count()
        elif status == "Archived":
            return ContractFiles.objects.filter(status=status).count()
    else:
        return ContractFiles.objects.count()
def date_converter(data):
    try:
        if data:
            return datetime.strptime(data, "%m/%d/%Y").strftime("%Y-%m-%d")
    except Exception as e:
        return data

@register.simple_tag
def date_converter(data):
    try:
        if data:
            return datetime.strptime(data, "%m/%d/%Y").strftime("%Y-%m-%d")
    except Exception as e:
        return data

@register.simple_tag
def get_by(user):
    if user:
        return f"{user.firstname} {user.lastname}"
    else:
        return ''

@register.simple_tag
def get_is_active(is_active):
    return mark_safe('<i class="fa fa-check-circle-o text-success f-18"></i>') \
        if is_active else mark_safe('<i class="fa fa-times-circle-o text-danger f-18"></i>')

@register.simple_tag
def status_color(status):
    if status == "Pending":
        return 'primary'
    elif status == "Reviewed":
        return 'danger'
    elif status == "Completed":
        return 'success'
    elif status == "Archived":
        return 'warning'

@register.simple_tag
def to_list_of_dict(data):
    if data:
        return json.loads(data)
    
@register.filter
def remove_documents_prefix(value):
    if value.startswith("/documents/"):
        return value[len("/documents/"):]
    return value
    

    