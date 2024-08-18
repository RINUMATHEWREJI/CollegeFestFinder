from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from students.models import Student
# Create your models here.
class Colleges(models.Model):
    college_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    contactno = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self,raw_password):
        return check_password(raw_password,self.password)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null=True, blank=True)  # Optional field for multi-day events
    event_venue = models.CharField(max_length=200)
    event_description = models.CharField(max_length=200)
    event_logo = models.ImageField(upload_to='event_logo/', null=True, blank=True)
    event_statuses = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    event_status = models.CharField(max_length=30, choices=event_statuses)
    
    students = models.ManyToManyField(Student, through='EventRegistration')

    def __str__(self):
        return self.event_name

    
class EventRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} registered for {self.event} on {self.registration_date}"
