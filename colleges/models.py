from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.apps import apps


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
    college = models.ForeignKey('colleges.Colleges', on_delete=models.CASCADE)
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null=True, blank=True)  
    event_venue = models.CharField(max_length=200)
    event_description = models.CharField(max_length=200)
    event_logo = models.ImageField(upload_to='event_logo/', null=True, blank=True)
    event_statuses = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    event_status = models.CharField(max_length=30, choices=event_statuses)
    event_pdf = models.FileField(upload_to='event_pdfs/', null=True, blank=True)

    students = models.ManyToManyField('students.Student', through='EventRegistration')

    def __str__(self):
        return self.event_name

    
class EventRegistration(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} registered for {self.event} on {self.registration_date}"

    

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_text = models.TextField()
    rating = models.IntegerField(default=0)  # Optional: Rating out of 5 or 10
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.student.name} for {self.event.event_name}"