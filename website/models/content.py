from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    designation_hi = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100)
    subject_hi = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=150)
    qualification_hi = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="teachers/", blank=True, null=True)
    description = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name


class Notice(models.Model):
    title = models.CharField(max_length=200)
    title_hi = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    description_hi = models.TextField(blank=True)
    notice_file = models.FileField(
        upload_to="notices/", blank=True, null=True
    )
    published_date = models.DateField(auto_now_add=True)
    expires_at = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=80, blank=True)
    category_hi = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class GalleryAlbum(models.Model):
    name = models.CharField(max_length=120)
    name_hi = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "name")

    def __str__(self):
        return self.name


class Gallery(models.Model):
    title = models.CharField(max_length=150)
    title_hi = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="gallery/")
    description = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    album = models.ForeignKey(
        GalleryAlbum,
        on_delete=models.SET_NULL,
        related_name="images",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self):
        return self.title


class InformationPage(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=160)
    title_hi = models.CharField(max_length=160, blank=True)
    content = models.TextField()
    content_hi = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    hero_eyebrow = models.CharField(max_length=160, blank=True)
    hero_eyebrow_hi = models.CharField(max_length=160, blank=True)
    hero_heading = models.CharField(max_length=220, blank=True)
    hero_heading_hi = models.CharField(max_length=220, blank=True)
    hero_description = models.TextField(blank=True)
    hero_description_hi = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    address_hi = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    public_email = models.EmailField(blank=True)
    office_hours = models.CharField(max_length=120, blank=True)
    office_hours_hi = models.CharField(max_length=120, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    map_embed_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Website settings"
        verbose_name_plural = "Website settings"

    def __str__(self):
        return "Website settings"


class CollegeLogo(models.Model):
    logo = models.ImageField(
        upload_to="college/logo/",
        verbose_name="College Logo"
    )

    class Meta:
        verbose_name = "College Logo"
        verbose_name_plural = "College Logo"

    def __str__(self):
        return "H.H. Inter College Logo"
