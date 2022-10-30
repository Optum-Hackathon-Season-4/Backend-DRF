from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


from .serializers import AppointmentSerializer, DoctorSerializer, FeedBackSerializer, HospitalSerializer, MedicineTestSerializer, OperationTestSerializer, PatientSerializer, PrescriptionSerializer, UserSerializer,ServicesSerializer
from .models import Allergy, Appointment, Feedback, Hospital,Doctor, MedicalTestAvailable, MedicineTest, OperationTest,Patient, Prescription, Services,MedicinesforPrescription,OperationsAvailable


from textblob import TextBlob



features = ["itching",
"skin_rash",
"nodal_skin_eruptions",
"continuous_sneezing",
"shivering",
"chills",
"joint_pain",
"stomach_pain",
"acidity",
"ulcers_on_tongue",
"muscle_wasting",
"vomiting",
"burning_micturition",
"spotting_ urination",
"fatigue",
"weight_gain",
"anxiety",
"cold_hands_and_feets",
"mood_swings",
"weight_loss",
"restlessness",
"lethargy",
"patches_in_throat",
"irregular_sugar_level",
"cough",
"high_fever",
"sunken_eyes",
"breathlessness",
"sweating",
"dehydration",
"indigestion",
"headache",
"yellowish_skin",
"dark_urine",
"nausea",
"loss_of_appetite",
"pain_behind_the_eyes",
"back_pain",
"constipation",
"abdominal_pain",
"diarrhoea",
"mild_fever",
"yellow_urine",
"yellowing_of_eyes",
"acute_liver_failure",
"fluid_overload",
"swelling_of_stomach",
"swelled_lymph_nodes",
"malaise",
"blurred_and_distorted_vision",
"phlegm",
"throat_irritation",
"redness_of_eyes",
"sinus_pressure",
"runny_nose",
"congestion",
"chest_pain",
"weakness_in_limbs",
"fast_heart_rate",
"pain_during_bowel_movements",
"pain_in_anal_region",
"bloody_stool",
"irritation_in_anus",
"neck_pain",
"dizziness",
"cramps",
"bruising",
"obesity",
"swollen_legs",
"swollen_blood_vessels",
"puffy_face_and_eyes",
"enlarged_thyroid",
"brittle_nails",
"swollen_extremeties",
"excessive_hunger",
"extra_marital_contacts",
"drying_and_tingling_lips",
"slurred_speech",
"knee_pain",
"hip_joint_pain",
"muscle_weakness",
"stiff_neck",
"swelling_joints",
"movement_stiffness",
"spinning_movements",
"loss_of_balance",
"unsteadiness",
"weakness_of_one_body_side",
"loss_of_smell",
"bladder_discomfort",
"foul_smell_of urine",
"continuous_feel_of_urine",
"passage_of_gases",
"internal_itching",
"toxic_look_(typhos)",
"depression",
"irritability",
"muscle_pain",
"altered_sensorium",
"red_spots_over_body",
"belly_pain",
"abnormal_menstruation",
"dischromic _patches",
"watering_from_eyes",
"increased_appetite",
"polyuria",
"family_history",
"mucoid_sputum",
"rusty_sputum",
"lack_of_concentration",
"visual_disturbances",
"receiving_blood_transfusion",
"receiving_unsterile_injections",
"coma",
"stomach_bleeding",
"distention_of_abdomen",
"history_of_alcohol_consumption",
"fluid_overload.1",
"blood_in_sputum",
"prominent_veins_on_calf",
"palpitations",
"painful_walking",
"pus_filled_pimples",
"blackheads",
"scurring",
"skin_peeling",
"silver_like_dusting",
"small_dents_in_nails",
"inflammatory_nails",
"blister",
"red_sore_around_nose",
"yellow_crust_ooze",
]


disease_to_specialization_mapping = {'fungal infection': 'dermatologist', 'allergy': 'allergist', 'gerd': 'gastroenterologist', 'chronic cholestasis': 'hepatologist', 'drug reaction': 'allergist', 'peptic ulcer diseae': 'gastroenterologist', 'aids': 'hiv specialist', 'diabetes ': 'endocrinologist', 'gastroenteritis': 'gastroenterologists', 'bronchial asthma': 'pulmonologist', 'hypertension ': 'cardiologist', 'migraine': 'neurologist', 'cervical spondylosis': 'neurosurgeon', 'paralysis (brain hemorrhage)': 'neurologist ', 'jaundice': 'gastroenterologist', 'malaria': 'infectionspecialist', 'chicken pox': 'infectionspecialist', 'dengue': 'infectionspecialist', 'typhoid': 'infectionspecialist', 'hepatitis a': 'hepatologist', 'hepatitis b': 'gastroenterologists', 'hepatitis c': 'hepatologist or gastroenterologist', 'hepatitis d': 'hepatologists', 'hepatitis e': 'hepatologists', 'alcoholic hepatitis': 'hepatologists', 'tuberculosis': 'pulmonologist', 'common cold': 'otolaryngologist.', 'pneumonia': 'pulmonologist', 'dimorphic hemmorhoids(piles)': 'proctologist', 'heart attack': 'cardiologist', 'varicose veins': 'phlebologists', 'hypothyroidism': 'endocrinologist', 'hyperthyroidism': 'endocrinologist', 'hypoglycemia': 'endocrinologist', 'osteoarthristis': 'orthopedist', 'arthritis': 'rheumatologist', '(vertigo) paroymsal  positional vertigo': 'otolaryngologist', 'acne': 'dermatologist', 'urinary tract infection': 'urologist', 'psoriasis': 'dermatologist', 'impetigo': 'dermatologist '}




# Create your views here.
def index(request):
    return HttpResponse("Server Working !!! ")



class HospitalView(APIView):
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals,many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


# Hospitals will be added and edited by admin only 
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    

    # Add Request
    def post(self, request):
        user = self.request.user
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            request.data.update({'patient' : patient.id})
            request.data.update({'approved' : False})
            serializer = FeedBackSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
        return Response({"message" : "You are not allowed to submit Feedbacks"},
        status = status.HTTP_401_UNAUTHORIZED)

    # Approve Request
    def put(self,request):
        user = self.request.user 
        if user.is_superuser:
            if request.data.get("id") is None: 
                return Response({"message" : "FeedBack ID is missing"},status = status.HTTP_400_BAD_REQUEST)
            elif len(Feedback.objects.filter(id = request.data.get("id"))) == 0:
                return Response({"message" : "ID not found in the database"})
            
            feedback = Feedback.objects.get(id = request.data.get("id"))
            feedback.approved = True 
            feedback.save()
            serializer = FeedBackSerializer(feedback)
            
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST )
        

        
        return Response({"message" : "You are not authorized for this operation"},status = status.HTTP_401_UNAUTHORIZED)


class OpenFeedBackViews(APIView):
    def get(self, request,id):
        
        if len(Doctor.objects.filter(id = id)) == 0:
            return Response({"message" : "Invalid Doctor ID"},status = status.HTTP_400_BAD_REQUEST)
        feedbacks = Feedback.objects.filter(doctor = Doctor.objects.get(id = id))
        serializer = FeedBackSerializer(feedbacks,many = True)
        return Response(serializer.data,status = status.HTTP_200_OK) 


class PrescriptionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,id = None):
        user = self.request.user 
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            prescriptions = Prescription.objects.filter(patient = patient)
            serializer = PrescriptionSerializer(prescriptions,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        if id is None: 
            return Response({"message": "Patient ID Missing"}, status = status.HTTP_400_BAD_REQUEST)
        elif len(Patient.objects.filter(id = id)) == 0 :
            return Response({"message" : "Patiend ID not in database"})
        patient = Patient.objects.get(id = id)
        prescriptions = Prescription.objects.filter(patient = patient)
        serializer = PrescriptionSerializer(prescriptions,many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request):
        user = self.request.user
        if user.is_superuser:
            if request.data.get('id') is None: 
                return Response({"message" : "Presciption ID is missing"},status = status.HTTP_400_BAD_REQUEST)
            elif len(Prescription.objects.filter(id = request.data.get('id'))) == 0:
                return Response({"message" : "Prescription ID not found in the database"},status = status.HTTP_400_BAD_REQUEST)
            
            prescription = Prescription.objects.get(id = request.data.get('id'))
            request.data.update({"days" : prescription.days})
            request.data.update({"follow_up" : prescription.follow_up})
            request.data.update({"symptoms" : prescription.symptoms})
            request.data.update({"patient" : prescription.patient.id})
            request.data.update({"doctor" : prescription.doctor.id})

            
            
            serializer = PrescriptionSerializer(prescription,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_200_OK )

        return Response({"Message" : "You are not allowed to do this operation"},status = status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = self.request.user 
        if user.is_doctor:
            if request.data.get('medicines') is None: 
                return Response({"message" : "Medicines are Missing"})
            request.data.update({'doctor' : Doctor.objects.get(doctor = user).id})
            serializer = PrescriptionSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()

                id = serializer.data['id']
                medicines = []
                for elem in request.data.get("medicines"):
                    a1 = MedicinesforPrescription(
                        name = elem["name"],
                        time_to_taken = elem["time_to_taken"],
                        cost = elem["cost"]
                    )
                    a1.save()
                    medicines.append(a1)
                prescription = Prescription.objects.get(id = id)
                prescription.medicines.set(medicines)
                serializer = PrescriptionSerializer(prescription)
                return Response(serializer.data, status = status.HTTP_201_CREATED) 

            return Response(serializer.errors, status = status.HTTP_200_OK)
            

        return Response({"message" : "You are not Authorized to do this operation"},status = status.HTTP_401_UNAUTHORIZED)
    

        
class MedicalTestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,id = None):
        user = self.request.user 
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            medicaltests = MedicineTest.objects.filter(patient = patient)
            serializer = MedicineTestSerializer(medicaltests,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        if id is None: 
            return Response({"message": "Patient ID Missing"}, status = status.HTTP_400_BAD_REQUEST)
        elif len(Patient.objects.filter(id = id)) == 0 :
            return Response({"message" : "Patiend ID not in database"})
        patient = Patient.objects.get(id = id)
        medicinetests = MedicineTest.objects.filter(patient = patient)
        serializer = MedicineTestSerializer(medicinetests,many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request):
        user = self.request.user
        if user.is_superuser:
            if request.data.get('id') is None: 
                return Response({"message" : "MedicineTests ID is missing"},status = status.HTTP_400_BAD_REQUEST)
            elif len(MedicineTest.objects.filter(id = request.data.get('id'))) == 0:
                return Response({"message" : "MedicinesTest ID not found in the database"},status = status.HTTP_400_BAD_REQUEST)
            
            medicinetest = MedicineTest.objects.get(id = request.data.get('id'))
            request.data.update({"patient" : medicinetest.patient.id})
            request.data.update({"doctor" : medicinetest.doctor.id})

            
            
            serializer = MedicineTestSerializer(medicinetest,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_200_OK )

        return Response({"Message" : "You are not allowed to do this operation"},status = status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = self.request.user 
        if user.is_doctor:
            if request.data.get('tests') is None: 
                return Response({"message" : "tests are Missing"})
            request.data.update({'doctor' : Doctor.objects.get(doctor = user).id})
            serializer = MedicineTestSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()

                id = serializer.data['id']
                tests = []
                for elem in request.data.get("tests"):
                    a1 = MedicalTestAvailable(
                        name = elem["name"],
                        recommendation = elem["recommendation"],
                        cost = elem["cost"]
                    )
                    a1.save()
                    tests.append(a1)
                medicinetests = MedicineTest.objects.get(id = id)
                medicinetests.tests.set(tests)
                serializer = MedicineTestSerializer(medicinetests)
                return Response(serializer.data, status = status.HTTP_201_CREATED) 

            return Response(serializer.errors, status = status.HTTP_200_OK)
            

        return Response({"message" : "You are not Authorized to do this operation"},status = status.HTTP_401_UNAUTHORIZED)
    
   

    

class OperationTestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,id = None):
        user = self.request.user 
        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            operationtest = OperationTest.objects.filter(patient = patient)
            serializer = OperationTestSerializer(operationtest,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        if id is None: 
            return Response({"message": "Patient ID Missing"}, status = status.HTTP_400_BAD_REQUEST)
        elif len(Patient.objects.filter(id = id)) == 0 :
            return Response({"message" : "Patiend ID not in database"})
        patient = Patient.objects.get(id = id)
        operations = OperationTest.objects.filter(patient = patient)
        serializer = OperationTestSerializer(operations,many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request):
        user = self.request.user
        if user.is_superuser:
            if request.data.get('id') is None: 
                return Response({"message" : "MedicineTests ID is missing"},status = status.HTTP_400_BAD_REQUEST)
            elif len(OperationTest.objects.filter(id = request.data.get('id'))) == 0:
                return Response({"message" : "MedicinesTest ID not found in the database"},status = status.HTTP_400_BAD_REQUEST)
            
            operationtest = OperationTest.objects.get(id = request.data.get('id'))
            request.data.update({"patient" : operationtest.patient.id})
            request.data.update({"doctor" : operationtest.doctor.id})

            
            
            serializer = OperationTestSerializer(operationtest,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_200_OK )

        return Response({"Message" : "You are not allowed to do this operation"},status = status.HTTP_401_UNAUTHORIZED)


    def post(self, request):
        user = self.request.user 
        if user.is_doctor:
            if request.data.get('operations') is None: 
                return Response({"message" : "operations are Missing"})
            request.data.update({'doctor' : Doctor.objects.get(doctor = user).id})
            serializer = OperationTestSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()

                id = serializer.data['id']
                tests = []
                for elem in request.data.get("operations"):
                    a1 = OperationsAvailable(
                        name = elem["name"],
                        recommendation = elem["recommendation"],
                        cost = elem["cost"]
                    )
                    a1.save()
                    tests.append(a1)
                operations = OperationTest.objects.get(id = id)
                operations.operations.set(tests)
                serializer = OperationTestSerializer(operations)
                return Response(serializer.data, status = status.HTTP_201_CREATED) 

            return Response(serializer.errors, status = status.HTTP_200_OK)
            

        return Response({"message" : "You are not Authorized to do this operation"},status = status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def get_reviews(request):
    if request.data.get("text") is None: 
        return Response({"message" : "No Test for Analysis"},status = status.HTTP_400_BAD_REQUEST)
    obj = TextBlob(request.data.get("text"))
    check_type = ""
    if obj.sentiment.polarity == 0: check_type = "neutral"
    elif obj.sentiment.polarity > 0: check_type = "positive"
    else: check_type = "neutral"
    return Response({
        "message" : check_type
    },status = status.HTTP_200_OK)
    # if request.data.get('id') is None: 
    #     return Response({"message" : "Doctor ID missing"},status = status.HTTP_400_BAD_REQUEST)
    # elif len(Doctor.objects.filter(id= request.data.get('id'))) == 0:
    #     return Response({"message" : "Invalid Doctor ID"},status = status.HTTP_400_BAD_REQUEST)
    # doctor = Doctor.objects.get( id = request.data.get('id'))
    # reviews = Feedback.objects.filter(doctor = doctor)
    # for review in reviews:
    #     obj = TextBlob(review.reviews)
    #     if obj.sentiment.polarity == 0: neutral += 1
    #     elif obj.sentiment.polarity < 0 : negative += 1
    #     else : positive += 1

    # return Response({
    #     "positive" : positive,
    #     "negative" : negative,
    #     "neutral" : neutral
    # },status = status.HTTP_200_OK)

@api_view(['POST'])
def doctor_recommendation(request):
    import os 
    print(os.listdir())
    from pycaret.classification import load_model,predict_model
    import pandas as pd
    data = {}
    for elem in features:
        data[elem] = []
        data[elem].append(0)
    for elem in request.data.keys():
        if elem in features: 
            data[elem].pop()
            data[elem].append(request.data.get(elem))
    df = pd.DataFrame(data)
    lr = load_model('lrmodelfile')
    predictions = predict_model(lr, data = df)    


    return Response({"Symptomps" : predictions['prediction_label'].values[0],
    "Specialization" : disease_to_specialization_mapping[predictions['prediction_label'].values[0].lower()].capitalize()},status = status.HTTP_200_OK)


