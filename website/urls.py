from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admission-enquiry/", views.admission_enquiry, name="admission_enquiry"),
    path("staff/login/", views.staff_login, name="staff_login"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/logout/", views.staff_logout, name="staff_logout"),
]
