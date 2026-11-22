from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import AdmissionEnquiryForm, ContactMessageForm
from .models import AdmissionEnquiry, ContactMessage, Gallery, Notice, Teacher


def home(request):
    gallery_images = Gallery.objects.filter(
        image__isnull=False
    ).order_by("-uploaded_at")
    teachers = Teacher.objects.filter(is_active=True).order_by("name")
    notices = Notice.objects.filter(is_active=True).order_by("-published_date")

    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("home")
        messages.error(request, "Please correct the errors below.")
    else:
        contact_form = ContactMessageForm()

    return render(request, "website/home.html", {
        "gallery_images": gallery_images,
        "teachers": teachers,
        "notices": notices,
        "contact_form": contact_form,
    })


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
        messages.error(request, "Please correct the errors below.")
    else:
        form = AdmissionEnquiryForm()

    return render(request, "website/admission_enquiry.html", {"form": form})


def staff_login(request):
    """Authenticate active Django staff accounts for the staff portal."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("staff_dashboard")
        raise PermissionDenied("Staff access is required.")

    form = AuthenticationForm(request, data=request.POST or None)
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not user.is_active or not user.is_staff:
            form.add_error(
                None,
                "This portal is available to authorised college staff only."
            )
        else:
            login(request, user)
            if url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("staff_dashboard")

    return render(request, "website/staff_login.html", {
        "form": form,
        "next": next_url,
    })


@login_required(login_url="staff_login")
def staff_dashboard(request):
    """A private overview page for authenticated staff and administrators."""
    if not request.user.is_staff:
        raise PermissionDenied("Staff access is required.")

    return render(request, "website/staff_dashboard.html", {
        "teacher_count": Teacher.objects.count(),
        "notice_count": Notice.objects.count(),
        "gallery_count": Gallery.objects.count(),
        "admission_count": AdmissionEnquiry.objects.count(),
        "message_count": ContactMessage.objects.count(),
    })


@login_required(login_url="staff_login")
@require_POST
def staff_logout(request):
    """Log out using a CSRF-protected POST request."""
    if not request.user.is_staff:
        raise PermissionDenied("Staff access is required.")
    logout(request)
    messages.success(request, "You have been signed out successfully.")
    return redirect("staff_login")
