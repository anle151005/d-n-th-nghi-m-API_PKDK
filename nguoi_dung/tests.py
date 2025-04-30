from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Patient, Appointment, Prescription
from datetime import datetime, timedelta

class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass123',
            is_staff=True
        )

    def test_create_patient(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'phone': '+84123456789',
            'address': 'Test Address',
            'date_of_birth': '1990-01-01',
            'blood_type': 'A+',
            'emergency_contact': 'Emergency Contact',
            'emergency_phone': '+84987654321'
        }
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

class AppointmentTests(APITestCase):
    def setUp(self):
        # Setup test data
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            phone='+84123456789',
            address='Test Address'
        )
        self.doctor = User.objects.create_user(
            username='doctor',
            password='doctorpass123',
            is_staff=True
        )

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'date': (datetime.now() + timedelta(days=1)).isoformat(),
            'symptoms': 'Test symptoms',
            'notes': 'Test notes'
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PrescriptionTests(APITestCase):
    def setUp(self):
        # Setup test data
        pass

    def test_create_prescription(self):
        # Add prescription tests
        pass
