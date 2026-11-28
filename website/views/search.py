from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from website.models import Gallery, InformationPage, Notice, Teacher


def site_search(request):
    query = request.GET.get("q", "").strip()[:100]
    notices = Notice.objects.none()
    teachers = Teacher.objects.none()
    pages = InformationPage.objects.none()
    gallery_images = Gallery.objects.none()

    if query:
        notices = Notice.objects.filter(
            is_active=True,
        ).filter(
            Q(expires_at__isnull=True)
            | Q(expires_at__gte=timezone.localdate())
        ).filter(
            Q(title__icontains=query)
            | Q(title_hi__icontains=query)
            | Q(description__icontains=query)
            | Q(description_hi__icontains=query)
        )
        teachers = Teacher.objects.filter(
            is_active=True,
        ).filter(
            Q(name__icontains=query)
            | Q(designation__icontains=query)
            | Q(subject__icontains=query)
            | Q(designation_hi__icontains=query)
            | Q(subject_hi__icontains=query)
            | Q(qualification_hi__icontains=query)
            | Q(description__icontains=query)
            | Q(description_hi__icontains=query)
        )
        pages = InformationPage.objects.filter(
            is_published=True,
        ).filter(
            Q(title__icontains=query)
            | Q(title_hi__icontains=query)
            | Q(content__icontains=query)
            | Q(content_hi__icontains=query)
        )
        gallery_images = Gallery.objects.filter(
            is_active=True,
        ).filter(
            Q(album__isnull=True) | Q(album__is_active=True)
        ).filter(
            Q(title__icontains=query)
            | Q(title_hi__icontains=query)
            | Q(description__icontains=query)
            | Q(description_hi__icontains=query)
        ).select_related("album")

    return render(request, "website/search/results.html", {
        "query": query,
        "notices": notices,
        "teachers": teachers,
        "pages": pages,
        "gallery_images": gallery_images,
    })
