from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.cmo.models import ChedOrders
# Register your models here.

@admin.register(ChedOrders)
class ChedOrdersAdmin(ModelAdmin):
    list_display = [ 'ra_num','description','compliance_category']
    list_filter = ['ra_num',]
    search_fields = ('ra_num',)
