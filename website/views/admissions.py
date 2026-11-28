from django.contrib import messages
from django.shortcuts import redirect, render

from website.forms import AdmissionEnquiryForm
from website.services.notifications import notify_college_staff


def admission_enquiry(request):
    language = request.session.get("site_language", "en")
    if request.method == "POST":
        form = AdmissionEnquiryForm(request.POST, language=language)
        if form.is_valid():
            enquiry = form.save()
            notify_college_staff(
                "New admission enquiry from the college website",
                (
                    f"Student: {enquiry.student_name}\n"
                    f"Class: {enquiry.class_applying_for}\n"
                    f"Mobile: {enquiry.mobile}\n"
                    f"Email: {enquiry.email}"
                ),
            )
            messages.success(
                request,
                (
                    "आपकी प्रवेश पूछताछ सफलतापूर्वक प्राप्त हो गई है।"
                    if language == "hi"
                    else "Your admission enquiry has been received successfully!"
                ),
            )
            return redirect("admission_enquiry")
        messages.error(
            request,
            (
                "कृपया नीचे दी गई त्रुटियाँ ठीक करें।"
                if language == "hi"
                else "Please correct the errors below."
            ),
        )
    else:
        form = AdmissionEnquiryForm(language=language)

    return render(request, "website/admission_enquiry.html", {"form": form})
