from django import forms

from website.models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
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

    def __init__(self, *args, language="en", **kwargs):
        super().__init__(*args, **kwargs)
        if language == "hi":
            labels = {
                "name": "पूरा नाम",
                "email": "ईमेल पता",
                "phone": "फ़ोन नंबर",
                "subject": "विषय",
                "message": "संदेश",
            }
            for field_name, label in labels.items():
                self.fields[field_name].label = label
            placeholders = {
                "name": "अपना पूरा नाम लिखें",
                "email": "अपना ईमेल पता लिखें",
                "phone": "अपना फ़ोन नंबर लिखें",
                "subject": "संदेश का विषय लिखें",
                "message": "अपना संदेश लिखें",
            }
            for field_name, placeholder in placeholders.items():
                self.fields[field_name].widget.attrs["placeholder"] = placeholder

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
