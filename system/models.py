from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random 
import string

def generate_key():
    passcode = list(string.ascii_lowercase + string.digits)
    random.shuffle(passcode)
    return "".join(passcode[:10])

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length = 200,blank = False, null = False)
    specialization = models.CharField(max_length = 200,blank = False, null = False)
    capacity = models.IntegerField(default = 0,blank = False, null = False)
    address = models.CharField(max_length = 300,blank = False, null = False)
    pass_key = models.CharField(unique = True, default = generate_key(),max_length = 100,blank = False, null = False)


class Allergy(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = False)
    symptoms = models.TextField()



class User(AbstractUser):
    is_patient = models.BooleanField(default = False)
    is_doctor = models.BooleanField(default = False)


class Patient(models.Model):

    MARITAL_CHOICES = (
        ("Married","Married"),
        ("Not Married","Not Married")
        )

    GENDER_CHOICES = (
        ("Male","Male"),
        ("Female","Female")
        )
    patient = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    birth_date = models.DateField(blank = False, null = False)
    name = models.CharField(max_length = 100,null = False, blank = False)
    age = models.IntegerField(default = 0, null = False, blank = False)
    marital_status = models.CharField(max_length = 40, choices = MARITAL_CHOICES,null = False, blank = False)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES,null = False, blank = False)
    address = models.CharField(max_length = 200, null = False, blank = False)
    income = models.IntegerField(default = 0, null = False, blank = False)
    allergic_history = models.ManyToManyField(Allergy)

class Doctor(models.Model):
    GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female")
    )
    doctor = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)

    hospital = models.ForeignKey(Hospital,on_delete = models.CASCADE,null = False, blank = False)
    name = models.CharField(max_length = 200, null = False, blank = False)
    age = models.IntegerField(default = 0, null = False, blank = False)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES,null = False, blank = False)
    specialization = models.CharField(max_length = 200,blank = False, null = False)
    consultation_charges = models.IntegerField(default = 0, null = False, blank = False)



