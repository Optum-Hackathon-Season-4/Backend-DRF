from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random 
import string
from django.core.validators import MaxValueValidator, MinValueValidator


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
    phone_number = models.CharField(max_length = 200)
    pass_key = models.CharField(unique = True, default = generate_key(),max_length = 100,blank = False, null = False)

    def __str__(self):
        return f'{self.id}-{self.name}'

class Allergy(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = False)
    symptoms = models.TextField()


    def __str__(self):
        return self.name



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
    phone_number = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100,null = False, blank = False)
    age = models.IntegerField(default = 0, null = False, blank = False)
    marital_status = models.CharField(max_length = 40, choices = MARITAL_CHOICES,null = False, blank = False)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES,null = False, blank = False)
    address = models.CharField(max_length = 200, null = False, blank = False)
    income = models.IntegerField(default = 0, null = False, blank = False)
    allergic_history = models.ManyToManyField(Allergy)

    def __str__(self):
        return f'{self.id}-{self.name}'

class Doctor(models.Model):
    GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female")
    )
    doctor = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)

    hospital = models.ForeignKey(Hospital,on_delete = models.CASCADE,null = False, blank = False)
    name = models.CharField(max_length = 200, null = False, blank = False)
    age = models.IntegerField(default = 0, null = False, blank = False)
    phone_number = models.CharField(max_length = 100)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES,null = False, blank = False)
    specialization = models.CharField(max_length = 200,blank = False, null = False)
    consultation_charges = models.IntegerField(default = 0, null = False, blank = False)

    def __str__(self):
        return f'{self.id}-{self.name}'

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, null = False, blank = False)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, null = False, blank = False)
    date = models.DateField(null = True, blank = True)
    approval = models.BooleanField(default = False, null = False, blank = False)

class Services(models.Model):
    SERVICE_CHOICES = (
        ("Medical Test","Medical Test"),
        ("Operation","Operation"),
        ("Drug","Drug")
    )

    name = models.CharField(max_length = 200,null = False, blank = False)
    cost = models.IntegerField(default = 0,null = False, blank = False)
    type = models.CharField(max_length = 100, choices = SERVICE_CHOICES)


    def __str__(self):
        return f'{self.id}-{self.name}'


class Feedback(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    treatment_rating = models.IntegerField(
        default = 0, null = False, blank = False, 
        validators = [MinValueValidator(0),MaxValueValidator(10)]
    )
    communication_rating = models.IntegerField(
        default = 0, null = False, blank = False, 
        validators = [MinValueValidator(0),MaxValueValidator(10)]

    )
    collaboration_rating = models.IntegerField(
        default = 0, null = False, blank = False, 
        validators = [MinValueValidator(0),MaxValueValidator(10)]
    )
    availability = models.IntegerField(
        default = 0, null = False, blank = False, 
        validators = [MinValueValidator(0),MaxValueValidator(10)]
    )
    reviews = models.TextField(blank = True, null = True)
    approved = models.BooleanField(default = False, null = False, blank = False)
    




