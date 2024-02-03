from django import forms
from clinic.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient, Appointment, MedicalEvent

class PatientLoginForm(AuthenticationForm):
    class Meta:
        model = Patient
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'middle_name', 'mothers_maiden_name', 'last_name', 'date_of_birth', 'gender', 'nationality',
                  'contact_number', 'emergency_contact_number', 'insurance', 'email', 'address', 'city', 'zip_code', 'state', 'country',
                  'profile_picture', 'height', 'weight', 'blood_type', 'allergies', 'notes', 'attachments']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'pattern': '\d*'}),
            'emergency_contact_number': forms.TextInput(attrs={'pattern': '\d*'}),
        }

from django import forms
from django.contrib.auth import get_user_model  
from .models import Patient

class UserForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model() 
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
    
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'description', 'location']
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