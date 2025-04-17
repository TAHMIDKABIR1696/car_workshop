from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mechanic(models.Model):
    id = models.AutoField(name="id", primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    id = models.AutoField(name="id", primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50, blank=True, null=True)
    car_license = models.CharField(max_length=20,blank=True, null=True)
    car_engine_number = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    id = models.AutoField(name="id", primary_key=True)
    appointment_date = models.DateField()
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    car_license = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return self.car_license
