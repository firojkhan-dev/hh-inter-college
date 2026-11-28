
from django.db import migrations


def create_default_information_pages(apps, schema_editor):
    InformationPage = apps.get_model("website", "InformationPage")

    pages = [
        {
            "slug": "about",
            "title": "About Us",
            "title_hi": "हमारे बारे में",
            "content": "Learn more about our college, its history, vision and mission.",
            "content_hi": "हमारे कॉलेज, उसके इतिहास, दृष्टिकोण और मिशन के बारे में जानें।",
            "is_published": True,
            "display_order": 1,
        },
        {
            "slug": "academics",
            "title": "Academics",
            "title_hi": "शैक्षणिक जानकारी",
            "content": "Explore our academic programs and educational activities.",
            "content_hi": "हमारे शैक्षणिक कार्यक्रमों और शैक्षिक गतिविधियों के बारे में जानें।",
            "is_published": True,
            "display_order": 2,
        },
        {
            "slug": "facilities",
            "title": "Facilities",
            "title_hi": "सुविधाएँ",
            "content": "Explore the facilities available at our college.",
            "content_hi": "हमारे कॉलेज में उपलब्ध सुविधाओं के बारे में जानें।",
            "is_published": True,
            "display_order": 3,
        },
    ]

    for page in pages:
        InformationPage.objects.get_or_create(
            slug=page["slug"],
            defaults=page,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_galleryalbum_informationpage_sitesettings_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_default_information_pages,
            migrations.RunPython.noop,
        ),
    ]
