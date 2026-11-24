
from django.contrib import admin
from .models import (
    Teacher,
    Notice,
    Gallery,
    ContactMessage,
    AdmissionEnquiry,
    CollegeLogo,
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "subject", "is_active")
    search_fields = ("name", "subject")
    list_filter = ("is_active",)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_at")
    search_fields = ("title",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at",)


@admin.register(AdmissionEnquiry)
class AdmissionEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "father_name",
        "class_applying_for",
        "mobile",
        "created_at",
    )
    search_fields = ("student_name", "father_name", "mobile")
    list_filter = ("class_applying_for", "created_at")
    readonly_fields = ("created_at",)




@admin.register(CollegeLogo)
class CollegeLogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo')