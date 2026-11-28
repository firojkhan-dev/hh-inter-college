from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from website.forms.staff import AdmissionStatusForm
from website.models import AdmissionEnquiry, ContactMessage, Gallery, Notice, Teacher


def _ensure_staff(request):
    if not request.user.is_staff:
        raise PermissionDenied("Staff access is required.")


def staff_login(request):
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
                "This portal is available to authorised college staff only.",
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
    _ensure_staff(request)
    context = {
        "teacher_count": Teacher.objects.count(),
        "notice_count": Notice.objects.count(),
        "gallery_count": Gallery.objects.count(),
        "admission_count": AdmissionEnquiry.objects.count(),
        "message_count": ContactMessage.objects.count(),
    }
    if request.user.has_perm("website.view_admissionenquiry"):
        context["recent_admissions"] = AdmissionEnquiry.objects.all()[:5]
    if request.user.has_perm("website.view_contactmessage"):
        context["recent_messages"] = ContactMessage.objects.all()[:5]
    return render(request, "website/staff_dashboard.html", context)


@login_required(login_url="staff_login")
def staff_admissions(request):
    _ensure_staff(request)
    if not request.user.has_perm("website.view_admissionenquiry"):
        raise PermissionDenied("Admission enquiry access is required.")

    status = request.GET.get("status", "")
    if status and status not in AdmissionEnquiry.Status.values:
        return HttpResponseBadRequest("Unknown admission enquiry status.")
    enquiries = AdmissionEnquiry.objects.all()
    if status in AdmissionEnquiry.Status.values:
        enquiries = enquiries.filter(status=status)
    paginator = Paginator(enquiries, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "website/staff/admissions.html", {
        "page_obj": page_obj,
        "status": status,
        "status_choices": AdmissionEnquiry.Status.choices,
    })


@login_required(login_url="staff_login")
@require_POST
def update_admission_status(request, pk):
    _ensure_staff(request)
    if not request.user.has_perm("website.change_admissionenquiry"):
        raise PermissionDenied("Admission update permission is required.")

    enquiry = get_object_or_404(AdmissionEnquiry, pk=pk)
    form = AdmissionStatusForm(request.POST, instance=enquiry)
    if form.is_valid():
        form.save()
        messages.success(request, "Admission enquiry status updated.")
    else:
        messages.error(request, "Please choose a valid enquiry status.")
    return redirect("staff_admissions")


@login_required(login_url="staff_login")
def staff_messages(request):
    _ensure_staff(request)
    if not request.user.has_perm("website.view_contactmessage"):
        raise PermissionDenied("Contact message access is required.")
    messages_page = Paginator(ContactMessage.objects.all(), 20).get_page(
        request.GET.get("page")
    )
    return render(request, "website/staff/messages.html", {
        "page_obj": messages_page,
    })


@login_required(login_url="staff_login")
@require_POST
def staff_logout(request):
    _ensure_staff(request)
    logout(request)
    messages.success(request, "You have been signed out successfully.")
    return redirect("staff_login")
