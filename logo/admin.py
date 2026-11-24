
from django.contrib import admin
from .models import CollegeLogo


@admin.register(CollegeLogo)
class CollegeLogoAdmin(admin.ModelAdmin):

    list_display = ('id', 'logo')

    def has_add_permission(self, request):
        return not CollegeLogo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
