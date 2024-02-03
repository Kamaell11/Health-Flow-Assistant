# Health Flow Assistant

Health Flow Assistant is a web application designed to streamline medical processes and improve patient care. It consists of several modules, including:

- `assistant`: Module for managing administrative tasks.
- `clinic`: Module for clinic-related functionalities.
- `doctor`: Module dedicated to doctor-specific features.
- `patient`: Module catering to patient-related operations.

# Description

After completing their studies, it is challenging for doctors to find employment in their field or specialization without relocating, resulting in patients waiting for specialists in their clinics or hospitals for a long time, especially in the National Health Fund (NFZ in Poland). There is a need for a space where meetings, consultations, treatment planning, and online prescription of necessary medications are efficiently carried out. An essential function would be for patients to regularly update detailed information, such as weight loss or occasional heart palpitations. Over time, patients may consider these details unimportant or forget about them, which can escape the attention of the doctor, affecting preventive care or influencing the course of treatment. With this application, doctors can prevent or more effectively treat current or future patient illnesses, continually improving their health and quality of life.

# Getting Started
- Clone the repository.
- Install project dependencies: 
## PiP
```
pip install -r requirements.txt.
```
## Conda
```
conda create --name your-env-name python=3.8
```
### or
```
conda install --file requirements.txt
```
### at last
```
conda activate your-env-name
```

## Run migrations:
 ```
 python manage.py makemigrations
 python manage.py migrate
 ```
- Start the development server: 
```
python manage.py runserver
```
# Usage
### CustomUser Model

The `CustomUser` model is an extension of the Django `AbstractUser` model. It introduces two additional boolean fields, `is_doctor` and `is_patient`, to identify the user's role. The `is_doctor` field is set to `True` for doctors, and the `is_patient` field is set to `True` for patients.

### Department Model

The `Department` model represents medical departments within the clinic. It includes fields such as `name` and `description` to provide information about the department.

### Specialization Model

The `Specialization` model represents medical specializations that doctors can have. It includes fields such as `name` and `description` to specify the specialization details.

### Doctor Model

The `Doctor` model extends the `CustomUser` model, representing a doctor in the system. It includes various fields like `gender`, `specialization`, `department`, `license_number`, `contact_number`, and more. This model stores essential information about doctors, including their profile picture, contact details, and professional information.

### Patient Model

The `Patient` model extends the `CustomUser` model, representing a patient in the system. It includes fields such as `first_name`, `last_name`, `date_of_birth`, `gender`, `contact_number`, and more. This model stores personal and health-related information about patients, including their profile picture, medical history, and contact details.

### Medication Model

The `Medication` model represents medications that can be prescribed to patients. It includes fields like `name`, `description`, `side_effects`, `dosage`, and `warnings` to provide comprehensive information about each medication.

### Prescription Model

The `Prescription` model represents a prescription created by a doctor for a specific patient. It includes fields such as `patient`, `issue_date`, `medications`, `dose`, `start_date`, `end_date`, `description`, and `attachments`. This model helps track prescribed medications and their details.

### MedicalEvent Model

The `MedicalEvent` model represents events related to a patient's medical history. It includes fields like `patient`, `event_type`, `date`, `description`, `attachments`, `prescriptions`, and `treatment`. This model helps document various medical events such as diseases, injuries, vaccinations, and more.

### MedicalHistory Model

The `MedicalHistory` model represents a comprehensive history of a patient's medical events. It includes fields like `patient`, `start_date`, `end_date`, `medical_events`, and `summary`. This model provides an overview of a patient's health history over a specified period.

### Appointment Model

The `Appointment` model represents scheduled appointments between patients and doctors. It includes fields such as `patient`, `doctor`, `appointment_date`, `description`, `status`, `location`, and `created_at`. This model helps manage appointments and their details.

# License
For now project is non-commercial, so
feel free to customize the content further based on your project's specific details and requirements.
