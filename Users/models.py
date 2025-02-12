from django.contrib.auth.models import AbstractUser,User
from django.db import models
import uuid
from django.conf import settings 

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('publicUser', 'User'),
        ('administrator', 'Administrator'),
        ('worker', 'Worker'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='publicUser')
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field

    def __str__(self):
        return f"{self.username} - {self.role}"
    
# ✅ Waste Report Model (User reports waste issues, assigned to workers by Admin)
class WasteReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports", limit_choices_to={'role': 'publicUser'})
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_reports", limit_choices_to={'role': 'administrator'},null=True,blank=True)
    image = models.ImageField(upload_to='waste_reports/', blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('resolved', 'Resolved'),
    ], default='pending')
    assigned_worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="report_tasks", limit_choices_to={'role': 'worker'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report by {self.user.username} - {self.status}"


# ✅ Waste Pickup Model (User schedules pickup, Admin assigns a worker)
class WastePickup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pickups", limit_choices_to={'role': 'publicUser'})
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_pickups", limit_choices_to={'role': 'administrator'})
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="pickup_tasks", limit_choices_to={'role': 'worker'})
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
    ], default='scheduled')

    def __str__(self):
        return f"Pickup at {self.location} on {self.date} - {self.status}"
