from django.contrib import admin
from django.urls import path, include 
from libraries.views import document_type_page, category_type_page, division_type_page, section_type_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('document_type/', document_type_page, name='libraries-document_type-page'),
    path('document_type/<slug:action>', document_type_page, name='libraries-document_type-page'),
    path('document_type/<slug:action>/<slug:pk>', document_type_page, name='libraries-document_type-page'),

    path('category_type/', category_type_page, name='libraries-category_type-page'),
    path('category_type/<slug:action>', category_type_page, name='libraries-category_type-page'),
    path('category_type/<slug:action>/<slug:pk>', category_type_page, name='libraries-category_type-page'),

    path('division_type/', division_type_page, name='libraries-division_type-page'),
    path('division_type/<slug:action>', division_type_page, name='libraries-division_type-page'),
    path('division_type/<slug:action>/<slug:pk>', division_type_page, name='libraries-division_type-page'),

    path('section_type/', section_type_page, name='libraries-section_type-page'),
    path('section_type/<slug:action>', section_type_page, name='libraries-section_type-page'),
    path('section_type/<slug:action>/<slug:pk>', section_type_page, name='libraries-section_type-page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
