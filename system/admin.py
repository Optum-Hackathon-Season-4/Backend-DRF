from django.contrib import admin
from .models import Allergy, Hospital,Patient,Doctor,User
# Register your models here.

admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Allergy)