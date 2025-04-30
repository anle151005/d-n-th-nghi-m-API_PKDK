from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Staff users can access any object
        if request.user.is_staff:
            return True
            
        # Check if the object has a user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # For Appointment objects
        if hasattr(obj, 'patient'):
            return obj.patient.user == request.user
            
        # For Prescription objects
        if hasattr(obj, 'appointment'):
            return obj.appointment.patient.user == request.user
            
        return False