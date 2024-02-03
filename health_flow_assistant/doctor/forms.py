from django import forms
from clinic.models import CustomUser as User
from .models import Doctor
from django.contrib.auth.forms import AuthenticationForm
from patient.models import Patient, Appointment, Prescription, MedicalEvent, Medication

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'department', 'license_number', 'contact_number', 'email', 'address', 'city', 'zip_code', 'state', 'country', 'profile_picture']
        widgets = {
            'contact_number': forms.TextInput(attrs={'pattern': '\d*'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        constraints = {
            'profile_picture': {
                'width': 500,
                'height': 500,
                'max_size': 1024 * 1024,
            }
        }

class UserForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation']
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            self.add_error('password_confirmation', "Passwords must match")

        return cleaned_data
    
class DoctorLoginForm(AuthenticationForm):
    class Meta:
        model = Doctor
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_date', 'description', 'location']
        widgets = {
            'patient': forms.HiddenInput(),
            'appointment_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Message (Optional)'}),
        }


class MedicalEventForm(forms.ModelForm):
    class Meta:
        model = MedicalEvent
        fields = ['event_type', 'date', 'description', 'attachments', 'treatment']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control-file'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Treatment (Optional)'}),
        }

class PrescriptionForm(forms.ModelForm):
    medications = forms.ModelMultipleChoiceField(
        queryset=Medication.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Prescription
        fields = ['issue_date', 'medications', 'dose', 'start_date', 'end_date', 'description', 'attachments']
        widgets = {
            'issue_date': forms.TextInput(attrs={'type': 'date'}),
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }
