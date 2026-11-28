from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from website.models import Notice


def _published_notices():
    today = timezone.localdate()
    return Notice.objects.filter(
        is_active=True,
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=today)
    )


def notice_list(request):
    query = request.GET.get("q", "").strip()[:100]
    notices = _published_notices()
    if query:
        notices = notices.filter(
            Q(title__icontains=query)
            | Q(title_hi__icontains=query)
            | Q(description__icontains=query)
            | Q(description_hi__icontains=query)
            | Q(category__icontains=query)
            | Q(category_hi__icontains=query)
        )
    page_obj = Paginator(notices.order_by("-published_date"), 20).get_page(
        request.GET.get("page")
    )
    return render(request, "website/notices/list.html", {
        "page_obj": page_obj,
        "query": query,
    })


def notice_detail(request, pk):
    notice = get_object_or_404(_published_notices(), pk=pk)
    return render(request, "website/notices/detail.html", {
        "notice": notice,
    })
