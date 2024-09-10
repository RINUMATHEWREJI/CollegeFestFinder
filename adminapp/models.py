from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.apps import apps
# Create your models here.

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contactno = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self,raw_password):
        return check_password(raw_password,self.password)
    
    def __str__(self):
        return self.name