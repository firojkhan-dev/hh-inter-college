from django.urls import path

from website.views import (
    staff_admissions,
    staff_dashboard,
    staff_login,
    staff_logout,
    staff_messages,
    update_admission_status,
)


urlpatterns = [
    path("staff/login/", staff_login, name="staff_login"),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),
    path("staff/admissions/", staff_admissions, name="staff_admissions"),
    path(
        "staff/admissions/<int:pk>/status/",
        update_admission_status,
        name="update_admission_status",
    ),
    path("staff/messages/", staff_messages, name="staff_messages"),
    path("staff/logout/", staff_logout, name="staff_logout"),
]
