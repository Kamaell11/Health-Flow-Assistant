from django.contrib import admin
from .models import Patient, Medication, Prescription, MedicalEvent, MedicalHistory, Appointment

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date_of_birth', 'gender', 'insurance', 'email', 'contact_number', 'emergency_contact_number', 'address', 'city', 'zip_code', 'state', 'country', 'profile_picture', 'height', 'weight', 'blood_type', 'allergies', 'notes', 'attachments', 'created_at']  
    
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'issue_date', 'display_medications', 'dose', 'start_date', 'end_date']  

    def display_medications(self, obj):
        return ', '.join([medication.name for medication in obj.medications.all()])

    display_medications.short_description = 'Medications'


class MedicalEventAdmin(admin.ModelAdmin):
    list_display = ['patient', 'event_type', 'date', 'description'] 

class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient']  

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'description']  

admin.site.register(Patient, PatientAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(MedicalEvent, MedicalEventAdmin)
admin.site.register(MedicalHistory, MedicalHistoryAdmin)
admin.site.register(Appointment, AppointmentAdmin)
