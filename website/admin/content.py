from django.contrib import admin

from website.models import (
    CollegeLogo,
    Gallery,
    GalleryAlbum,
    InformationPage,
    Notice,
    SiteSettings,
    Teacher,
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "subject", "display_order", "is_active")
    search_fields = ("name", "subject", "designation")
    list_filter = ("is_active", "subject")
    ordering = ("display_order", "name")
    fieldsets = (
        ("English", {
            "fields": ("name", "designation", "subject", "qualification")
        }),
        ("Hindi", {
            "fields": ("designation_hi", "subject_hi", "qualification_hi")
        }),
        ("Profile", {"fields": ("photo", "description", "description_hi")}),
        ("Display", {"fields": ("display_order", "is_active")}),
    )


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_date", "expires_at", "is_active")
    search_fields = ("title", "title_hi", "description", "description_hi")
    list_filter = ("is_active", "category", "published_date", "expires_at")
    readonly_fields = ("published_date",)
    fieldsets = (
        ("English", {"fields": ("title", "description", "category")}),
        ("Hindi", {"fields": ("title_hi", "description_hi", "category_hi")}),
        ("Publishing", {
            "fields": ("notice_file", "published_date", "expires_at", "is_active")
        }),
    )


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name", "name_hi")
    list_filter = ("is_active",)
    readonly_fields = ("created_at",)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "uploaded_at", "is_active")
    search_fields = ("title", "title_hi", "description", "description_hi")
    list_filter = ("is_active", "album", "uploaded_at")
    autocomplete_fields = ("album",)
    readonly_fields = ("uploaded_at",)


@admin.register(InformationPage)
class InformationPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "display_order", "updated_at")
    search_fields = ("title", "title_hi", "slug", "content", "content_hi")
    list_filter = ("is_published", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("updated_at",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("English homepage content", {
            "fields": (
                "hero_eyebrow", "hero_heading", "hero_description",
                "address", "office_hours",
            )
        }),
        ("Hindi homepage content", {
            "fields": (
                "hero_eyebrow_hi", "hero_heading_hi", "hero_description_hi",
                "address_hi", "office_hours_hi",
            )
        }),
        ("Contact and social links", {
            "fields": (
                "phone", "public_email", "facebook_url",
                "instagram_url", "youtube_url", "map_embed_url",
            )
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CollegeLogo)
class CollegeLogoAdmin(admin.ModelAdmin):
    list_display = ("id", "logo")
