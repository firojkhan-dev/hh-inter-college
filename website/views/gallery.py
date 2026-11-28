from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from website.models import Gallery, GalleryAlbum


def gallery_list(request):
    albums = GalleryAlbum.objects.filter(is_active=True)
    selected_album = None
    images = Gallery.objects.filter(
        is_active=True,
        image__isnull=False,
    ).filter(
        Q(album__isnull=True) | Q(album__is_active=True)
    ).select_related("album").order_by("-uploaded_at")

    album_id = request.GET.get("album")
    if album_id:
        selected_album = get_object_or_404(albums, pk=album_id)
        images = Gallery.objects.filter(
            is_active=True,
            image__isnull=False,
            album=selected_album,
        ).order_by("-uploaded_at")

    page_obj = Paginator(images, 24).get_page(request.GET.get("page"))
    return render(request, "website/gallery/list.html", {
        "albums": albums,
        "selected_album": selected_album,
        "page_obj": page_obj,
    })
