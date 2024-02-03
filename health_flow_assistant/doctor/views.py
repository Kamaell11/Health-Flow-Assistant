from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from doctor.forms import DoctorForm, UserForm, DoctorLoginForm, AppointmentForm
from doctor.forms import MedicalEventForm, PrescriptionForm

from .models import Doctor, Department, Specialization
from django.shortcuts import render, redirect, get_object_or_404
from patient.models import Patient, Appointment , MedicalHistory, MedicalEvent, Prescription, Medication

def doctor_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_doctor = True 
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('doctor:doctor_dashboard')  

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'doctor/register.html', {'user_form': user_form, 'doctor_form': doctor_form})

def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('doctor:doctor_dashboard')  
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = DoctorLoginForm()

    return render(request, 'doctor/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required(login_url='login') 
def doctor_dashboard(request):
    if request.user.is_doctor:
        return render(request, 'doctor/dashboard.html')
    else:
        return render(request, 'access_denied.html')
    
from django.contrib.auth import get_user_model

def doctors_count(request):
    doctors_count = get_user_model().objects.filter(is_doctor=True).count()
    return {'doctors_count': doctors_count}


def specializations_count(request):
    specializations_count = Doctor.objects.values('specialization').distinct().count()
    return {'specializations_count': specializations_count}


def departments_list(request):
    departments_list = Department.objects.all()

    return {'departments_list': departments_list}

def doctors_section(request):
    doctors_list = Doctor.objects.all()[:4]  
    return ({'doctors_list': doctors_list})




@login_required  
def doctor_appointments(request):
    current_doctor = request.user

    appointments = Appointment.objects.filter(doctor=current_doctor)

    context = {'appointments': appointments}
    return render(request, 'doctor/doctor_appointments.html', context)


def patients_list(request):
    query = request.GET.get('q', '')
    if query:
        # Perform a filtered query based on the search query
        patient_list = Patient.objects.filter(user__username__icontains=query)
    else:
        # Retrieve all patients if no search query is provided
        patient_list = Patient.objects.all()

    return render(request, 'doctor/patients_list.html', {'patient_list': patient_list, 'query': query})


def medical_history_list(request):
    medical_history_list = MedicalHistory.objects.all()
    return render(request, 'doctor/medical_history_list.html', {'medical_history_list': medical_history_list})

def medical_history_detail(request, history_id):
    medical_history = get_object_or_404(MedicalHistory, id=history_id)
    return render(request, 'doctor/medical_history_detail.html', {'medical_history': medical_history})

def prescription_list(request):
    prescription_list = Prescription.objects.all()
    return render(request, 'doctor/prescription_list.html', {'prescription_list': prescription_list})

def prescription_detail(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'doctor/prescription_detail.html', {'prescription': prescription})

def add_medical_event(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = MedicalEventForm(request.POST)
        if form.is_valid():
            medical_event = form.save(commit=False)
            medical_event.patient = patient
            medical_event.save()
            return redirect('doctor:medical_history_list')
    else:
        form = MedicalEventForm()

    return render(request, 'doctor/add_medical_event.html', {'form': form, 'patient': patient})

def add_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    current_doctor = request.user
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.doctor = current_doctor
            prescription.save()
            form.save_m2m()  # Save the medications relation
            return redirect('doctor:prescription_list')
    else:
        form = PrescriptionForm()

    return render(request, 'doctor/add_prescription.html', {'form': form, 'patient': patient})


from django.http import Http404

@login_required(login_url='login')
def cancel_appointment_doctor(request, appointment_id):
    try:
        if request.user.is_doctor:
            doctor = request.user.doctor
            appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)


            if appointment:
                appointment.delete()
                messages.success(request, 'Appointment canceled successfully.')
            else:
                messages.error(request, 'Error: Appointment not found or you are not authorized to cancel it.')
        else:
            messages.error(request, 'Error: You are not authorized to perform this action.')

    except Doctor.DoesNotExist:
        raise Http404("No Doctor matches the given query.")

    return redirect('doctor:appointments')

@login_required(login_url='login')
def reschedule_appointment_doctor(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment rescheduled successfully.')
            return redirect('patient:view_appointments')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'doctor/reschedule_appointment.html', {'form': form, 'appointment_id': appointment_id, 'appointment': appointment})
