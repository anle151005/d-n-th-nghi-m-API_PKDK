from rest_framework import serializers
from .models import Patient, Appointment, Prescription
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class PatientSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['user']
        
    def validate_phone(self, value):
        if Patient.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['status']

    def validate_date(self, value):
        # Add your date validation logic here
        return value

    def validate(self, data):
        # Add your cross-field validation here
        return data

class AppointmentSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = UserSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)
    
    class Meta:
        model = Prescription
        fields = '__all__'

    def validate_medicine(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Medicine must be a list of medications")
        return value
        
