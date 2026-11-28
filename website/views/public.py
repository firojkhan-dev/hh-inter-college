from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db.models import Q

from website.forms import ContactMessageForm
from website.models import Gallery, Notice, Teacher
from website.services.notifications import notify_college_staff


def home(request):
    language = request.session.get("site_language", "en")
    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST, language=language)
        if contact_form.is_valid():
            contact_message = contact_form.save()
            notify_college_staff(
                "New contact message from the college website",
                (
                    f"Name: {contact_message.name}\n"
                    f"Email: {contact_message.email}\n"
                    f"Phone: {contact_message.phone}\n"
                    f"Subject: {contact_message.subject}\n\n"
                    f"{contact_message.message}"
                ),
            )
            messages.success(
                request,
                (
                    "आपका संदेश प्राप्त हो गया है।"
                    if language == "hi"
                    else "Your message has been received."
                ),
            )
            return redirect("home")
        messages.error(
            request,
            (
                "कृपया नीचे दी गई त्रुटियाँ ठीक करें।"
                if language == "hi"
                else "Please correct the errors below."
            ),
        )
    else:
        contact_form = ContactMessageForm(language=language)

    today = timezone.localdate()
    notices = Notice.objects.filter(
        is_active=True,
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=today)
    ).order_by("-published_date")[:3]

    return render(request, "website/home.html", {
        "gallery_images": Gallery.objects.filter(
            is_active=True,
            image__isnull=False,
        ).filter(
            Q(album__isnull=True) | Q(album__is_active=True)
        ).select_related("album").order_by("-uploaded_at")[:12],
        "teachers": Teacher.objects.filter(
            is_active=True,
        ).order_by("display_order", "name"),
        "notices": notices,
        "contact_form": contact_form,
    })
