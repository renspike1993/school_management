from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django.utils.html import format_html
from .models import Registrar
from .models import Folder


@admin.register(Registrar)
class RegistrarAdmin(ModelAdmin):
    list_display = ['school', 'category', 'created_at']
    list_filter = ['school', 'category', 'created_at']
    search_fields = ['school__school_name', 'school__abbreviation', 'category']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Registrar Information', {
            'fields': ('school', 'category')
        }),
        ('System Info', {
            'fields': ('created_at',)
        }),
    )

    ordering = ['-created_at']


@admin.register(Folder)
class FolderAdmin(ModelAdmin):
    list_display = [
        'folder_name',
        'registrar',
        'cabinet',
        'floor',
        'created_at',
    ]

    list_filter = [
        'created_at',
        'registrar',
    ]

    search_fields = [
        'folder_name',
        'cabinet',
        'floor',
        # 'description',
        # 'registrar__first_name',
        # 'registrar__middle_name',
        # 'registrar__last_name',
        # 'registrar__school__school_name',
    ]

    readonly_fields = ['created_at']

    fieldsets = (
        ('Folder Information', {
            'fields': ('registrar', 'folder_name','cabinet','floor',)
        }),
        ('System Info', {
            'fields': ('created_at',)
        }),
    )

    ordering = ['-created_at']