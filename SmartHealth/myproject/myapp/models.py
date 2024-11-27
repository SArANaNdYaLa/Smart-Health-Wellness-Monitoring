from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Doctor Model
class Doctor(models.Model):
    STATUS_CHOICES = [
        ('on_hold', 'On Hold'),
        ('permanent', 'Permanent'),
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_hold')

    def __str__(self):
        return self.name


# Patient Model
class Patient(models.Model):
    STATUS_CHOICES = [
        ('on_hold', 'On Hold'),
        ('admitted', 'Admitted'),
    ]

    name = models.CharField(max_length=100)
    symptoms = models.TextField()
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_hold')

    def __str__(self):
        return self.name


# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"Appointment with {self.doctor.name} for {self.patient.name} on {self.appointment_date}"


# WellnessTransaction Model
class WellnessTransaction(models.Model):
    CATEGORY_CHOICES = [
        ('diet', 'Diet'),
        ('fitness', 'Fitness'),
        ('medical', 'Medical'),
        ('other', 'Other'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.category.capitalize()}: {self.amount} on {self.date}"


# HealthData Model
"""from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class HealthData(models.Model):
    ACTIVITY_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')
    heart_rate = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    sleep_hours = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    steps = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    calories_burned = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    hydration = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    activity_level = models.CharField(max_length=50, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HealthData({self.user.username}, {self.timestamp})"""
