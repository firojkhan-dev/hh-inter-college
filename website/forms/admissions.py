from django import forms

from website.models import AdmissionEnquiry


class AdmissionEnquiryForm(forms.ModelForm):
    class Meta:
        model = AdmissionEnquiry
        fields = [
            "student_name",
            "father_name",
            "class_applying_for",
            "mobile",
            "email",
            "address",
        ]
        widgets = {
            "student_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter student name",
            }),
            "father_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter father's name",
            }),
            "class_applying_for": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter class",
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter mobile number",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email address",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter full address",
                "rows": 4,
            }),
        }

    def __init__(self, *args, language="en", **kwargs):
        super().__init__(*args, **kwargs)
        if language == "hi":
            labels = {
                "student_name": "विद्यार्थी का नाम",
                "father_name": "पिता का नाम",
                "class_applying_for": "किस कक्षा में प्रवेश चाहिए",
                "mobile": "मोबाइल नंबर",
                "email": "ईमेल पता",
                "address": "पूरा पता",
            }
            for field_name, label in labels.items():
                self.fields[field_name].label = label
            placeholders = {
                "student_name": "विद्यार्थी का नाम लिखें",
                "father_name": "पिता का नाम लिखें",
                "class_applying_for": "कक्षा का नाम लिखें",
                "mobile": "मोबाइल नंबर लिखें",
                "email": "ईमेल पता लिखें",
                "address": "पूरा पता लिखें",
            }
            for field_name, placeholder in placeholders.items():
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
