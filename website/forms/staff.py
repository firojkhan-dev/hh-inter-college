from django import forms

from website.models import AdmissionEnquiry


class AdmissionStatusForm(forms.ModelForm):
    class Meta:
        model = AdmissionEnquiry
        fields = ["status", "internal_notes"]
        widgets = {
            "internal_notes": forms.Textarea(attrs={"rows": 2}),
        }
