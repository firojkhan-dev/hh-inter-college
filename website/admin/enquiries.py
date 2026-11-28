from django.contrib import admin

from website.models import AdmissionEnquiry, ContactMessage


@admin.register(AdmissionEnquiry)
class AdmissionEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "class_applying_for",
        "mobile",
        "status",
        "created_at",
    )
    search_fields = ("student_name", "father_name", "mobile", "email")
    list_filter = ("status", "class_applying_for", "created_at")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Student and guardian", {
            "fields": (
                "student_name", "father_name", "class_applying_for",
                "mobile", "email", "address",
            )
        }),
        ("Staff workflow", {
            "fields": ("status", "internal_notes", "created_at", "updated_at")
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("is_read", "created_at")
    readonly_fields = ("created_at",)
