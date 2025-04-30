from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, Appointment, Prescription
from .serializers import (
    PatientSerializer, 
    AppointmentSerializer, 
    PrescriptionSerializer,
    AppointmentCreateSerializer
)
from .permissions import IsOwnerOrStaff
import logging

logger = logging.getLogger(__name__)

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blood_type']
    search_fields = ['user__username', 'phone', 'address']
    ordering_fields = ['created_at', 'user__username']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(f"Patient created by user {self.request.user.username}")

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'date']
    ordering_fields = ['date', 'status']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(patient__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return AppointmentCreateSerializer
        return AppointmentSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if appointment.status == 'SCHEDULED':
            appointment.status = 'CANCELLED'
            appointment.save()
            logger.info(f"Appointment {pk} cancelled by {request.user.username}")
            return Response({'status': 'appointment cancelled'})
        return Response(
            {'error': 'Cannot cancel non-scheduled appointment'},
            status=status.HTTP_400_BAD_REQUEST
        )

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Prescription.objects.all()
        return Prescription.objects.filter(appointment__patient__user=self.request.user)
