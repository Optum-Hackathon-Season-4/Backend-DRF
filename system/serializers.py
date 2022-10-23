from rest_framework import serializers
from .models import Allergy, Hospital,Doctor,Patient,User

class HospitalSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Hospital
        fields = ['id','name','specialization','capacity','address']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id','name','age','gender','specialization','consultation_charges','hospital']

class AllergySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Allergy
        fields = ['name','symptoms']

class PatientSerializer(serializers.ModelSerializer):
    allergic_history = AllergySerializer(many = True,read_only = True)
    class Meta : 
        model = Patient
        fields = ['id','birth_date','name','age','marital_status','gender','address','income','allergic_history']
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username','email','is_patient','is_doctor']
        extra_kwargs = {
            'password' : {'write_only' : True} 
        }

