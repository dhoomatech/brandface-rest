from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from .models import Enquiry

# Resource for export
class EnquiryResource(resources.ModelResource):
    class Meta:
        model = Enquiry
        fields = ('id', 'business_card__business_name', 'name', 'email', 'phone', 'message', 'created_at')
        export_order = ('id', 'business_card__business_name', 'name', 'email', 'phone', 'message', 'created_at')

# Admin class with export and filters
class EnquiryAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EnquiryResource

    list_display = ('id', 'business_card', 'name', 'email', 'phone', 'created_at')
    list_filter = ('business_card', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')

admin.site.register(Enquiry, EnquiryAdmin)
