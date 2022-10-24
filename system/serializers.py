from rest_framework import serializers
from .models import Allergy, Appointment, Feedback, Hospital,Doctor, MedicalTestAvailable, MedicineTest, MedicinesforPrescription, OperationTest, OperationsAvailable,Patient, Prescription,User,Services
import datetime
from django.db.models import Avg


class HospitalSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, data):
        doctors = Doctor.objects.filter(hospital = data)
        return Feedback.objects.filter(doctor__in = doctors).aggregate(Avg('treatment_rating'))['treatment_rating__avg']
    

    class Meta: 
        model = Hospital
        fields = ['id','name','specialization','capacity','address','phone_number','rating']
        read_only_fields = ('rating',)

class DoctorSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer( read_only = True)
    passkey = serializers.CharField(max_length = 20,write_only = True)
    treatment_rating = serializers.SerializerMethodField()
    communication_rating = serializers.SerializerMethodField()
    collaboration_rating = serializers.SerializerMethodField()
    availability_rating = serializers.SerializerMethodField()


    def get_treatment_rating(self, data):
        return Feedback.objects.filter(doctor = data).aggregate(Avg('treatment_rating'))['treatment_rating__avg']

    def get_communication_rating(self, data):
        return Feedback.objects.filter(doctor = data).aggregate(Avg('communication_rating'))['communication_rating__avg']

    def get_collaboration_rating(self, data):
        return Feedback.objects.filter(doctor = data).aggregate(Avg('collaboration_rating'))['collaboration_rating__avg']
    
    def get_availability_rating(self, data):
        return Feedback.objects.filter(doctor = data).aggregate(Avg('availability'))['availability__avg']




    class Meta:
        model = Doctor
        fields = ['id','name','age','gender','specialization','consultation_charges','hospital','passkey','phone_number','treatment_rating',
        'communication_rating','collaboration_rating','availability_rating']
        read_only_fields = ('hospital','treatment_rating','communication_rating','collaboration_rating','availability_rating')
        extra_kwargs = {
            'passkey': {'write_only': True},
        }

    def validate(self, data):
        desired_hospital = Hospital.objects.filter(pass_key = data.get("passkey"))
        if len(desired_hospital) == 0:
            raise serializers.ValidationError("Pass Key is Invalid")
        data.update({'hospital':desired_hospital[0]})
        del data['passkey']

        return super().validate(data)


class AllergySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Allergy
        fields = ['name','symptoms']



class PatientSerializer(serializers.ModelSerializer):
    allergic_history = AllergySerializer(many = True,read_only = True)
    class Meta : 
        model = Patient
        fields = ['id','birth_date','name','age','marital_status','gender','address','income','allergic_history','phone_number']
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username','email','is_patient','is_doctor']
        extra_kwargs = {
            'password' : {'write_only' : True} 
        }

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Appointment
        fields = ['id','doctor','patient','date','approval']

    def validate(self, data):
        if data.get('patient') is None or data.get('doctor') is None or data.get('date') is None: 
            raise serializers.ValidationError("Patient or Doctors are missing")

        doctor = data.get('doctor')
        patient = data.get('patient')
        date = data.get('date')

        now = datetime.datetime.now().date()
        if now >= date : 
            raise serializers.ValidationError("This Date is Not Allowed!!!")
        appointments = Appointment.objects.filter(doctor = doctor,patient = patient, date = date)
        if len(appointments)  > 0 :
            raise serializers.ValidationError("This Appointment is Already in the Queue!!!!")
        return super().validate(data)

class ServicesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Services
        fields = '__all__'

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
    
    def validate(self, data):
        if data.get('patient') is not None and data.get('doctor') is not None: 
            feedbacks = Feedback.objects.filter(patient = data.get('patient'),doctor = data.get('doctor'))
            if len(feedbacks) > 0: 
                raise serializers.ValidationError("Feedback already added by this patient")
            return super().validate(data)
        raise serializers.ValidationError("Patient or Doctor Missing")



class MedicineSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MedicinesforPrescription
        fields = ['name','time_to_taken','cost']


class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = MedicineSerializer(many = True, read_only = True)
    class Meta:
        model = Prescription
        fields = ['id','days','follow_up','date',
        'symptoms','payment_deadline','paid','patient','doctor','medicines']

class MedicalTestAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTestAvailable
        fields = ['name','recommendation','cost']

class MedicineTestSerializer(serializers.ModelSerializer):
    tests = MedicalTestAvailableSerializer(many = True, read_only = True)
    class Meta:
        model = MedicineTest
        fields = ['id','patient','doctor','tests','payment_deadline','paid']

class OperationsAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationsAvailable
        fields = ['name','recommendation','cost']
    
class OperationTestSerializer(serializers.ModelSerializer):
    operations = OperationsAvailableSerializer(many = True, read_only = True)
    class Meta:
        model = OperationTest
        fields = ['id','patient','doctor','operations','payment_deadline','paid']
    

