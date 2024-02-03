from django.db import models

from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

INSURANCE_STATUS = [
    ('Y', 'Insured'),
    ('N', 'Non-Insured'),
    ('DK', 'No info'),
]

BLOOD_TYPE_CHOICES = [
        ('A+', 'A positive'),
        ('A-', 'A negative'),
        ('B+', 'B positive'),
        ('B-', 'B negative'),
        ('AB+', 'AB positive'),
        ('AB-', 'AB negative'),
        ('O+', 'O positive'),
        ('O-', 'O negative'),
    ]
from clinic.models import CustomUser 

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=40, blank=True)
    mothers_maiden_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True)
    date_of_death = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    nationality = models.CharField(max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Nationality')])
    contact_number = PhoneNumberField(region='PL')
    emergency_contact_number = PhoneNumberField(blank=True)
    insurance = models.CharField(max_length=2, choices=INSURANCE_STATUS, default='DK')
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Country')])
    profile_picture = models.ImageField(blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    allergies = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    attachments = models.FileField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Medication(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    dosage = models.CharField(max_length=125, blank=True)
    warnings = models.TextField(blank=True)
    attachments = models.FileField(blank=True)


    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    issue_date = models.DateTimeField()
    medications = models.ManyToManyField(Medication)
    dose = models.CharField(max_length=125)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    attachments = models.FileField(blank=True)
    doctor = models.ForeignKey(get_user_model(),null=True, on_delete=models.CASCADE)  



    def __str__(self):
        return f"{self.medications} - {self.dose}"

class MedicalEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('D', 'Disease'),
        ('S', 'Sickness'),
        ('I', 'Injury'),
        ('W', 'Weight'),
        ('H', 'Height'),
        ('BP', 'Blood Pressure'),
        ('HR', 'Heart Rate'),
        ('O', 'Other'),
        ('A', 'Allergy'),
        ('V', 'Vaccination'),
        ('C', 'Checkup'),
        ('M', 'Medication'),
        ('E', 'Exercise'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=2, choices=EVENT_TYPE_CHOICES)
    date = models.DateField()
    description = models.TextField()
    attachments = models.FileField(blank=True)
    prescriptions = models.ManyToManyField(Prescription, related_name='events', blank=True)
    treatment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_event_type_display()} for {self.patient}"

    
class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True, help_text='Start date of the medical history')
    end_date = models.DateField(null=True, blank=True, help_text='End date of the medical history')
    medical_events = models.ManyToManyField(MedicalEvent, blank=True)
    summary = models.TextField(blank=True, help_text='Summary or assessment of the patient\'s medical history')

    def __str__(self):
        return f"Medical history for {self.patient} ({self.start_date} - {self.end_date})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('S', 'Scheduled'),
        ('C', 'Completed'),
        ('X', 'Canceled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  
    appointment_date = models.DateTimeField()
    description = models.TextField(blank=True, help_text='Additional details about the appointment')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    location = models.CharField(max_length=100, blank=True, help_text='Location or room for the appointment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} on {self.appointment_date}, at {self.location}"
        
