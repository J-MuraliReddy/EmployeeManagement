from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    work_assigned = models.BooleanField(default=False)
    work_description = models.TextField(blank=True, null=True)
    work_file = models.FileField(upload_to='work_files/', blank=True, null=True)
    notification_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # Handle manually
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated

    def __str__(self):
        return self.name


class Work(models.Model):
    description = models.TextField()  # Description of the work to be assigned
    assigned = models.BooleanField(default=False)  # Indicates if the work is assigned
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign Key to Employee
    assigned_at = models.DateTimeField(default=timezone.now)  # Timestamp when the work was assigned
    due_date = models.DateTimeField(null=True, blank=True)  # Due date for the work, if applicable
    file = models.FileField(upload_to='work_files/', blank=True, null=True)  # Work-related files
    assigned_date = models.DateTimeField(default=timezone.now) # Date work was assigned


    def __str__(self):
        return f"Work for {self.assigned_to.name if self.assigned_to else 'Unassigned'}"
