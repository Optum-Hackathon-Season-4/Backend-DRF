import re
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .serializers import AppointmentSerializer, DoctorSerializer, FeedBackSerializer, HospitalSerializer, PatientSerializer, UserSerializer,ServicesSerializer
from .models import Allergy, Appointment, Hospital,Doctor,Patient, Services

# Create your views here.
def index(request):
    return HttpResponse("Server Working !!! ")



# Hospitals will be added and edited by admin only 
class HospitalView(APIView):
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals,many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class HospitalDatabaseView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        user = self.request.user
        if user.is_superuser:
            serializer = HospitalSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "You are not allowed to do this operation "},status = status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        user = self.request.user
        if user.is_superuser:
            if request.data.get('id') is None: 
                return Response({"message" : "Hospital ID Missing!!!"},status = status.HTTP_400_BAD_REQUEST)
            elif len(Hospital.objects.filter(id = request.data.get('id'))) == 0 : 
                return Response({"message" : "Hospital ID Missing in the Database"},status = status.HTTP_400_BAD_REQUEST)
            else: 
                hospital = Hospital.objects.get(id = request.data.get('id'))
                serializer = HospitalSerializer(hospital , data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "You are not allowed to perform this operation"},status = status.HTTP_401_UNAUTHORIZED)
    


class DoctorView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class PatientView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class UserRegistrationView(APIView):
    # Edit Doctor Serializers and Patient Serializers for Validation
    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if request.data.get('password') is None: 
            return Response({"message" : "Password Missing!!"},status = status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        password = make_password(password = password)

        if user_serializer.is_valid():
            if request.data.get("is_patient") is True: 
                parent_serializer = PatientSerializer(data = request.data)
            elif request.data.get("is_doctor") is True: 
                parent_serializer = DoctorSerializer(data = request.data)
            else: 
                return Response({"message" : "Type of User in Request Missing"},status = status.HTTP_400_BAD_REQUEST)
            

            if parent_serializer.is_valid():
                if request.data.get("is_patient") is True: 
                    user = user_serializer.save(password = password)
                    parent_serializer.save(patient = user)
                    return Response(parent_serializer.data, status = status.HTTP_201_CREATED)
                else: 
                    user = user_serializer.save(password = password)
                    parent_serializer.save(doctor = user)
                    return Response(parent_serializer.data, status = status.HTTP_201_CREATED)
            else: 
                return Response(parent_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        else: 
            return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class SpecificPatientView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        user = self.request.user
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status = status.HTTP_200_OK)
        elif user.is_doctor: 
            if request.data.get("id") is None: 
                return Response({"message": "Patient ID is Required"},status = status.HTTP_400_BAD_REQUEST)
            try:
                patient = Patient.objects.get(id = request.data.get("id"))
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except: 
                return Response({"message" : "Invalid Patient ID"},status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "Invalid User!!"},status = status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = self.request.user 
        if user.is_patient: 
            try: 
                allergic_data = []
                for elem in request.data.get("allergies"):
                    a1 = Allergy(
                        name = elem["name"],
                        symptoms = elem["symptoms"]
                    )
                    a1.save()
                    allergic_data.append(a1)
                patient = Patient.objects.get(patient = user)
                patient.allergic_history.set(allergic_data) 
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except: 
                return Response({"message" : "Allergies were not Provided"},status = status.HTTP_400_BAD_REQUEST)
            

        
        return Response({"message" : "Invalid User!!"},status = status.HTTP_400_BAD_REQUEST)


class SpecificDoctorView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        user = self.request.user
        if user.is_doctor: 
            doctor = Doctor.objects.get(doctor = user)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status = status.HTTP_200_OK)
        elif user.is_patient: 
            if request.data.get("id") is None: 
                return Response({"message": "Doctor ID is Required"},status = status.HTTP_400_BAD_REQUEST)
            try:
                doctor = Doctor.objects.get(id = request.data.get("id"))
                serializer = DoctorSerializer(doctor)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except: 
                return Response({"message" : "Invalid Doctor ID"},status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "Invalid User!!"},status = status.HTTP_400_BAD_REQUEST)


class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Get Appointment
    def get(self, request):
        user = self.request.user 
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            appointments = Appointment.objects.filter(patient = patient)
            serializer = AppointmentSerializer(appointments,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else: 
            doctor = Doctor.objects.get(doctor = user)
            appointments = Appointment.objects.filter(doctor = doctor)
            serializer = AppointmentSerializer(appointments,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

    # Book Appointment
    def post(self, request):
        user = self.request.user
        if user.is_patient:
            patient = Patient.objects.get(patient = user)
            request.data.update({'patient' : patient.id})
            serializer = AppointmentSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST )

        
        return Response({"message" : "You can't Book Appointments" },status = status.HTTP_401_UNAUTHORIZED)

    # Approve Appointment 
    def put(self, request):
        user = self.request.user 
        if user.is_doctor: 
            if request.data.get('id') is None: 
                return Response({"message" : "Appintment ID is missing!!"},status = status.HTTP_400_BAD_REQUEST)
            try:
                appointment = Appointment.objects.get(id = request.data.get('id'))
                appointment.approval = True 
                appointment.save()
                serializer = AppointmentSerializer(appointment)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except: 
                return Response({"message" : "Appointment ID is invalid!!"},status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "You are not allowed to do this operation"},status = status.HTTP_401_UNAUTHORIZED)

class ServicesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        user = self.request.user
        if user.is_doctor or user.is_superuser:
            services = Services.objects.all()
            serializer = ServicesSerializer(services,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"Message" : "You are not authorized to access this"},status = status.HTTP_401_UNAUTHORIZED)


    def post(self, request):
        user = self.request.user 
        if user.is_superuser:
            serializer = ServicesSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = self.request.user 
        if user.is_superuser: 
            if request.data.get('id') is None: 
                return Response({"message" : "Service ID Missing!!!"},status = status.HTTP_400_BAD_REQUEST)
            elif len(Services.objects.filter(id = request.data.get('id'))) == 0 : 
                return Response({"message" : "Service ID Missing in the Database"},status = status.HTTP_400_BAD_REQUEST)
            else: 
                service = Services.objects.get(id = request.data.get('id'))
                serializer = ServicesSerializer(service , data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "You are not allowed to perform this operation"},status = status.HTTP_401_UNAUTHORIZED)
           
        

class FeedBackView(APIView):
    def post(self, request):
        user = self.request.user
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            request.data.update({'patient' : patient.id})
            serializer = FeedBackSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
        return Response({"message" : "You are not allowed to submit Feedbacks"},
        status = status.HTTP_401_UNAUTHORIZED)




        
    

