
from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    qualification = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="teachers/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    notice_file = models.FileField(
        upload_to="notices/", blank=True, null=True
    )
    published_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="gallery/")
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AdmissionEnquiry(models.Model):

    student_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    class_applying_for = models.CharField(max_length=50)

    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name



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