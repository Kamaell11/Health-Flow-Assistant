from django.urls import path
from .views import patient_register, patient_login, patient_dashboard, make_appointment, view_medical_history, view_prescriptions, view_medical_events, view_appointments, view_profile, view_appointments, doctors_list, cancel_appointment, reschedule_appointment, add_medical_event 

app_name = 'patient'

urlpatterns = [
    path('login/', patient_login, name='patient_login'),
    path('register/', patient_register, name='patient_register'),
    path('dashboard/', patient_dashboard, name='patient_dashboard'),
    path('medical-history/', view_medical_history, name='view_medical_history'),
    path('prescriptions/', view_prescriptions, name='view_prescriptions'),
    path('medical-events/', view_medical_events, name='view_medical_events'),
    path('add-medical-event/<int:patient_id>/', add_medical_event, name='add_medical_event'),
    path('appointments/', view_appointments, name='view_appointments'),
    path('profile/', view_profile, name='view_profile'),
    path('appointments/make/', make_appointment, name='make_appointment'),  # Add this line
    path('appointments/cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
    path('appointments/reschedule/<int:appointment_id>/', reschedule_appointment, name='reschedule_appointment'),
    path('doctors/', doctors_list, name='doctors_list'),
    # Dodaj inne URL-e dla widoków pacjenta, jeśli są dostępne
]
