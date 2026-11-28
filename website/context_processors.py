from logo.models import CollegeLogo
from website.models import InformationPage, SiteSettings

def college_logo(request):
    return {
        "college_logo": CollegeLogo.objects.first(),
        "site_settings": SiteSettings.objects.first(),
        "site_language": request.session.get("site_language", "en"),
        "published_pages": InformationPage.objects.filter(
            is_published=True
        ).order_by("display_order", "title"),
    }