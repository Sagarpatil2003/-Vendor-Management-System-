from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class PurchaseOrderInline(admin.StackedInline):
    model = PurchaseOrder
    extra = 0 

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'average_response_time', 'fulfillment_rate')
    search_fields = ('name', 'vendor_code')
    inlines = [PurchaseOrderInline]

admin.site.register(Vendor, VendorAdmin)

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'order_data', 'delivery_data', 'status')
    list_filter = ('status', 'vendor')
    search_fields = ('po_number', 'vendor__name')

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillmet_rate')
    list_filter = ('vendor',)
    search_fields = ('vendor__name', 'date')
    readonly_fields= ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillmet_rate')
    

admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)
