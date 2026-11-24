
from django.db import models


class CollegeLogo(models.Model):

    logo = models.ImageField(
        upload_to='college/logo/',
        verbose_name="College Logo"
    )

    class Meta:
        verbose_name = "College Logo"
        verbose_name_plural = "College Logo"

    def __str__(self):
        return "H.H. Inter College Logo"
