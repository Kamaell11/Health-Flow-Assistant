from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from patient.forms import PatientForm, UserForm, PatientLoginForm, AppointmentForm, MedicalEventForm
from .models import Appointment, Patient, MedicalHistory, MedicalEvent, Prescription, Medication
from doctor.models import Doctor, Department, Specialization
from django.db.models import Q

def patient_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_patient = True 
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()

            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('patient:patient_dashboard')

    else:
        user_form = UserForm()
        patient_form = PatientForm()

    return render(request, 'patient/register.html', {'user_form': user_form, 'patient_form': patient_form})

def patient_login(request):
    if request.method == 'POST':
        form = PatientLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('patient:patient_dashboard')  
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = PatientLoginForm()

    return render(request, 'patient/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required(login_url='login') 
def patient_dashboard(request):

    if request.user.is_patient:
        return render(request, 'patient/dashboard.html')
    else:

        return render(request, 'access_denied.html')
    
from django.contrib.auth import get_user_model

def patients_count(request):
    patients_count = get_user_model().objects.filter(is_patient=True).count()
    return {'patients_count': patients_count}

def appointments_count(request):
    appointments_count = Appointment.objects.count()
    return {'appointments_count': appointments_count}

@login_required(login_url='login')
def make_appointment(request):
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('patient:view_appointments')
    else:
        appointment_form = AppointmentForm()

    return render(request, 'patient/make_appointment.html', {'appointment_form': appointment_form})



@login_required(login_url='login')
def view_medical_history(request):
    user = request.user
    if user.is_patient:
        medical_history = MedicalHistory.objects.filter(patient=user.patient)
        return render(request, 'patient/medical_history.html', {'medical_history': medical_history})
    else:
        return render(request, 'access_denied.html')

@login_required(login_url='login')
def view_prescriptions(request):
    user = request.user
    if user.is_patient:
        prescriptions = Prescription.objects.filter(patient=user.patient)
        return render(request, 'patient/prescriptions.html', {'prescriptions': prescriptions})
    else:
        return render(request, 'access_denied.html')

@login_required(login_url='login')
def view_medical_events(request):
    user = request.user
    if user.is_patient:
        medical_events = MedicalEvent.objects.filter(patient=user.patient)
        return render(request, 'patient/medical_events.html', {'medical_events': medical_events})
    else:
        return render(request, 'access_denied.html')

@login_required(login_url='login')
def view_appointments(request):
    user = request.user
    if user.is_patient:
        appointments = Appointment.objects.filter(patient=user.patient)
        return render(request, 'patient/appointments.html', {'appointments': appointments})
    else:
        return render(request, 'access_denied.html')
    

@login_required(login_url='login')
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    appointment.delete()
    messages.success(request, 'Appointment canceled successfully.')
    return redirect('patient:view_appointments')

@login_required(login_url='login')
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment rescheduled successfully.')
            return redirect('patient:view_appointments')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'patient/reschedule_appointment.html', {'form': form, 'appointment_id': appointment_id})


@login_required(login_url='login')
def view_profile(request):
    user = request.user
    return render(request, 'patient/profile.html', {'user': user})

def doctors_list(request):
    query = request.GET.get('q')
    specialization_filter = request.GET.get('specialization')
    department_filter = request.GET.get('department')

    doctors_list = Doctor.objects.all()
    specializations = Specialization.objects.all()
    departments = Department.objects.all()

    if query:
        doctors_list = doctors_list.filter(
            Q(user__username__icontains=query) |
            Q(department__name__icontains=query) |
            Q(specialization__name__icontains=query)
        )

    if specialization_filter:
        doctors_list = doctors_list.filter(specialization__name=specialization_filter)

    if department_filter:
        doctors_list = doctors_list.filter(department__name=department_filter)

    return render(request, 'patient/doctors_list.html', {
        'doctors_list': doctors_list,
        'specializations': specializations,
        'departments': departments,
        'query': query,
        'specialization_filter': specialization_filter,
        'department_filter': department_filter,
    })

@login_required(login_url='login')
def add_medical_event(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = MedicalEventForm(request.POST, request.FILES)
        if form.is_valid():
            medical_event = form.save(commit=False)
            medical_event.patient = patient
            medical_event.save()
            return redirect('patient:view_medical_events')

    else:
        form = MedicalEventForm()

    return render(request, 'patient/add_medical_event.html', {'form': form, 'patient': patient})