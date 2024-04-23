from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, CheckboxInput
from django import forms
from libraries.models import DocumentType, CategoryType, DivisionType


class DocumentTypeForm(ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name','is_active']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document name'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_documenttype(self):
        name = self.cleaned_data['name']
        r = DocumentType.objects.filter(name=name).first()
        if r:
            raise ValidationError("Document name already exist")
        return name
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['oninput'] = 'this.value = this.value.toUpperCase();'


class CategoryTypeForm(ModelForm):
    class Meta:
        model = CategoryType
        fields = ['name', 'is_active']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_categorytype(self):
        name = self.cleaned_data['name']
        r = CategoryType.objects.filter(name=name).first()
        if r:
            raise ValidationError("Category name already exist")
        return name
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['oninput'] = 'this.value = this.value.toUpperCase();'
    
class DivisionTypeForm(ModelForm):
    class Meta:
        model = DivisionType
        fields = ['name', 'is_active']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter division name'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_divisiontype(self):
        name = self.cleaned_data['name']
        r = DivisionType.objects.filter(name=name).first()
        if r:
            raise ValidationError("Division name already exist")
        return name
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['oninput'] = 'this.value = this.value.toUpperCase();'