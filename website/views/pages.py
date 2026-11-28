from django.shortcuts import get_object_or_404, render

from website.models import InformationPage


def information_page(request, slug):
    page = get_object_or_404(
        InformationPage,
        slug=slug,
        is_published=True,
    )
    return render(request, "website/pages/detail.html", {"page": page})
