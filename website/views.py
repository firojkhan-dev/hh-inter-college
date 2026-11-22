
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Gallery, Teacher, Notice
from .forms import ContactMessageForm, AdmissionEnquiryForm


def home(request):

    # Gallery Images
    gallery_images = Gallery.objects.filter(
        image__isnull=False
    ).order_by("-uploaded_at")

    # Active Teachers
    teachers = Teacher.objects.filter(
        is_active=True
    ).order_by("name")

    # Active Notices
    notices = Notice.objects.filter(
        is_active=True
    ).order_by("-published_date")

    # Contact Form Submission
    if request.method == "POST":

        contact_form = ContactMessageForm(request.POST)

        if contact_form.is_valid():

            contact_form.save()

            messages.success(
                request,
                "Your message has been sent successfully!"
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        contact_form = ContactMessageForm()

    context = {
        "gallery_images": gallery_images,
        "teachers": teachers,
        "notices": notices,
        "contact_form": contact_form,
    }

    return render(
        request,
        "website/home.html",
        context
    )


def admission_enquiry(request):

    if request.method == "POST":

        form = AdmissionEnquiryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your admission enquiry has been submitted successfully!"
            )

            return redirect("admission_enquiry")

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = AdmissionEnquiryForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "website/admission_enquiry.html",
        context
    )