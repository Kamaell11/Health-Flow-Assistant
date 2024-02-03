from django.db import models

from clinic.models import CustomUser
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    contact_number = PhoneNumberField(region='PL')
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Country')])
    nationality = models.CharField(max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Nationality')])
    profile_picture = models.ImageField(blank=True, upload_to='doctor_profile_pics/')
    notes = models.TextField(blank=True)
    attachments = models.FileField(blank=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"
    
    

