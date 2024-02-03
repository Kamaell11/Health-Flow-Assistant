from django.contrib import admin
from .models import Doctor, Department, Specialization

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'license_number']  
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'license_number']
    list_filter = ['specialization', 'department']
    list_per_page = 10

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Specialization, SpecializationAdmin)
