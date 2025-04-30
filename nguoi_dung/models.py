from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Patient(TimeStampedModel):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='patients'
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Số điện thoại phải có định dạng: '+999999999'. Tối đa 15 chữ số."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    date_of_birth = models.DateField()
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('O+', 'O+'), ('O-', 'O-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
        ]
    )
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"

class Appointment(TimeStampedModel):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )
    date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )
    symptoms = models.TextField()
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date}"

class Prescription(TimeStampedModel):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescription'
    )
    medicine = models.JSONField()  # Store structured medicine data
    instructions = models.TextField()
    dosage = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    next_visit = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Prescription')
        verbose_name_plural = _('Prescriptions')

    def __str__(self):
        return f"Prescription for {self.appointment}"
