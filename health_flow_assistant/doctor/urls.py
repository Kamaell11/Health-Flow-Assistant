from django.urls import path
from .views import doctor_register, doctor_login, doctor_dashboard, doctor_appointments, patients_list, medical_history_list, medical_history_detail, prescription_list, prescription_detail, add_medical_event, add_prescription, cancel_appointment_doctor, reschedule_appointment_doctor
app_name = 'doctor'

urlpatterns = [
    path('register/', doctor_register, name='doctor_register'),
    path('login/', doctor_login, name='doctor_login'),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor_appointments/', doctor_appointments, name='doctor_appointments'),
    path('patients/', patients_list, name='patients_list'),
    path('medical-history/', medical_history_list, name='medical_history_list'),
    path('medical-history/<int:history_id>/', medical_history_detail, name='medical_history_detail'),
    path('prescriptions/', prescription_list, name='prescription_list'),
    path('prescriptions/<int:prescription_id>/', prescription_detail, name='prescription_detail'),
    path('add-medical-event/<int:patient_id>/', add_medical_event, name='add_medical_event'),
    path('add-prescription/<int:patient_id>/', add_prescription, name='add_prescription'),
    path('cancel_appointment_doctor/<int:appointment_id>/', cancel_appointment_doctor, name='cancel_appointment_doctor'),
    path('reschedule_appointment_doctor/<int:appointment_id>/', reschedule_appointment_doctor, name='reschedule_appointment_doctor'),
]



