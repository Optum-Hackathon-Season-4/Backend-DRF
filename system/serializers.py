from rest_framework import serializers
from .models import Allergy, Appointment, Feedback, Hospital,Doctor,Patient,User,Services
import datetime

class HospitalSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Hospital
        fields = ['id','name','specialization','capacity','address','phone_number']


class DoctorSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer( read_only = True)
    passkey = serializers.CharField(max_length = 20,write_only = True)
    class Meta:
        model = Doctor
        fields = ['id','name','age','gender','specialization','consultation_charges','hospital','passkey','phone_number']
        read_only_fields = ('hospital',)
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
        
        

