from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    

    path("admission-enquiry/",views.admission_enquiry,name="admission_enquiry"),
]