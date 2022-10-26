"""connecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import HospitalDatabaseView, MedicalTestView, OperationTestView, PatientView, PrescriptionView, ServicesView, SpecificDoctorView, UserRegistrationView, index,HospitalView,DoctorView,SpecificPatientView,AppointmentView,FeedBackView,OpenFeedBackViews,get_reviews,doctor_recommendation
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path("",index, name = "index"),
    path('hospital/',HospitalView.as_view(),name="hospital"),
    path("doctor/",DoctorView.as_view(),name = "doctor"),
    path("patient/",PatientView.as_view(),name = "patient"),
    path('specificpatientview/',SpecificPatientView.as_view(),name = "specificpatient"),
    path('specificdoctorview/',SpecificDoctorView.as_view(),name= "specificdoctor"),
    path('appointments/',AppointmentView.as_view(),name = "appointments"),
    path("feedback/",FeedBackView.as_view(),name="feedbacks"),
    path('openfeedback/',OpenFeedBackViews.as_view(),name="openfeedback"),
    
    
    path('prescriptions/',PrescriptionView.as_view(),name="prescription"),
    path('medicaltests/',MedicalTestView.as_view(),name = "medicaltest"),
    path('operations/',OperationTestView.as_view(),name = "operationtest"),

    path("signup/",UserRegistrationView.as_view(),name = "registration"),
    path("login/",obtain_auth_token,name ="login"),
    path("hospitaldatabaseview/",HospitalDatabaseView.as_view(),name = "hospitaldatabaseview"),
    path("servicesview/",ServicesView.as_view(),name = "services"),
    path("reviews/",get_reviews,name = "reviews"),
    path("doctor_recommendation",doctor_recommendation,name = "doctor_recommendation")


]
