
from django import forms
from .models import ContactMessage, AdmissionEnquiry


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number",
            }),

            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter subject",
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your message here...",
                "rows": 5,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Name must contain at least 3 characters."
            )

        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "Message must contain at least 10 characters."
            )

        return message


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
