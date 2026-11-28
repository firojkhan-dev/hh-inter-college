from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from website.models import (
    AdmissionEnquiry,
    ContactMessage,
    Gallery,
    GalleryAlbum,
    InformationPage,
    Notice,
    SiteSettings,
    Teacher,
)


User = get_user_model()


class PublicPageTests(TestCase):
    def test_header_shows_branding_and_teacher_navigation(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="logo-mark"')
        self.assertContains(response, "H.H. Inter College")
        self.assertContains(response, 'aria-controls="navLinks"')
        self.assertContains(response, 'href="/#teachers">Teachers</a>')

    def test_favicon_redirects_to_the_existing_svg_asset(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            "/static/website/img/favicon.svg",
        )

    def test_admission_links_use_the_enquiry_page(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<header class="header">')
        self.assertContains(response, '<footer class="main-footer">')
        self.assertContains(
            response,
            f'href="{reverse("admission_enquiry")}" class="nav-btn"',
        )
        self.assertContains(response, "Admission Enquiry")

    def test_invalid_contact_submission_is_not_styled_as_success(self):
        response = self.client.post(reverse("home"), {
            "name": "x", "email": "invalid", "phone": "",
            "subject": "", "message": "short",
        })
        self.assertContains(response, 'class="error-message"')
        self.assertNotContains(response, 'class="success-message"')

    def test_invalid_admission_submission_is_not_styled_as_success(self):
        response = self.client.post(reverse("admission_enquiry"), {})
        self.assertContains(response, 'class="alert alert-error"')
        self.assertNotContains(response, 'class="alert alert-success"')

    def test_admission_page_uses_shared_site_layout(self):
        response = self.client.get(reverse("admission_enquiry"))
        self.assertContains(response, '<header class="header">')
        self.assertContains(response, '<footer class="main-footer">')
        self.assertContains(response, 'class="admission-form"')


class StaffAuthenticationTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="college-staff",
            password="Strong-Test-Password-927!",
            is_staff=True,
        )
        self.student_user = User.objects.create_user(
            username="student-user",
            password="Strong-Test-Password-927!",
            is_staff=False,
        )

    def test_staff_login_page_is_available(self):
        response = self.client.get(reverse("staff_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/staff_login.html")
        self.assertContains(response, 'class="brand-logo"')
        self.assertContains(response, "website/img/college-school-mark.png")

    def test_dashboard_redirects_anonymous_visitors_to_login(self):
        response = self.client.get(reverse("staff_dashboard"))
        self.assertRedirects(
            response,
            f'{reverse("staff_login")}?next={reverse("staff_dashboard")}',
        )

    def test_staff_can_login_and_open_dashboard(self):
        response = self.client.post(reverse("staff_login"), {
            "username": "college-staff",
            "password": "Strong-Test-Password-927!",
        })
        self.assertRedirects(response, reverse("staff_dashboard"))
        dashboard = self.client.get(reverse("staff_dashboard"))
        self.assertEqual(dashboard.status_code, 200)
        self.assertTemplateUsed(dashboard, "website/staff_dashboard.html")

    def test_non_staff_account_cannot_login_to_staff_portal(self):
        response = self.client.post(reverse("staff_login"), {
            "username": "student-user",
            "password": "Strong-Test-Password-927!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_non_staff_user_is_forbidden_from_dashboard(self):
        self.client.force_login(self.student_user)
        response = self.client.get(reverse("staff_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_staff_logout_requires_post_and_ends_session(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("staff_logout"))
        self.assertRedirects(response, reverse("staff_login"))
        dashboard = self.client.get(reverse("staff_dashboard"))
        self.assertEqual(dashboard.status_code, 302)


class DynamicWebsiteFeatureTests(TestCase):
    def test_notice_archive_hides_expired_and_inactive_notices(self):
        current_notice = Notice.objects.create(
            title="Current notice",
            description="Current description",
            expires_at=timezone.localdate(),
        )
        Notice.objects.create(
            title="Expired notice",
            description="Expired description",
            expires_at=timezone.localdate() - timedelta(days=1),
        )
        Notice.objects.create(
            title="Draft notice",
            description="Draft description",
            is_active=False,
        )

        response = self.client.get(reverse("notice_list"))

        self.assertContains(response, current_notice.title)
        self.assertNotContains(response, "Expired notice")
        self.assertNotContains(response, "Draft notice")

    def test_notice_detail_uses_hindi_content_when_available(self):
        notice = Notice.objects.create(
            title="English title",
            title_hi="हिंदी शीर्षक",
            description="English body",
            description_hi="हिंदी विवरण",
        )
        session = self.client.session
        session["site_language"] = "hi"
        session.save()

        response = self.client.get(
            reverse("notice_detail", args=[notice.pk])
        )

        self.assertContains(response, "हिंदी शीर्षक")
        self.assertContains(response, "हिंदी विवरण")

    def test_search_finds_hindi_notice_fields(self):
        Notice.objects.create(
            title="School update",
            title_hi="विद्यालय सूचना",
            description="A public notice",
        )
        session = self.client.session
        session["site_language"] = "hi"
        session.save()

        response = self.client.get(
            reverse("site_search"),
            {"q": "विद्यालय"},
        )

        self.assertContains(response, "विद्यालय सूचना")

    def test_default_information_pages_are_published(self):
        page = InformationPage.objects.get(slug="about")

        response = self.client.get(
            reverse("information_page", args=[page.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, page.title)

    def test_gallery_album_filter_shows_only_its_images(self):
        album = GalleryAlbum.objects.create(name="Annual Day")
        other_album = GalleryAlbum.objects.create(name="Sports Day")
        matching_image = Gallery.objects.create(
            title="Stage",
            image=SimpleUploadedFile("stage.jpg", b"image"),
            album=album,
        )
        Gallery.objects.create(
            title="Ground",
            image=SimpleUploadedFile("ground.jpg", b"image"),
            album=other_album,
        )

        response = self.client.get(
            reverse("gallery_list"),
            {"album": album.pk},
        )

        self.assertContains(response, matching_image.title)
        self.assertNotContains(response, "Ground")

    def test_gallery_search_finds_matching_caption(self):
        Gallery.objects.create(
            title="Classroom",
            title_hi="कक्षा",
            image=SimpleUploadedFile("classroom.jpg", b"image"),
        )

        response = self.client.get(
            reverse("site_search"),
            {"q": "कक्षा"},
        )

        self.assertContains(response, "कक्षा")

    def test_unpublished_information_page_returns_not_found(self):
        page = InformationPage.objects.create(
            slug="draft-page",
            title="Draft page",
            content="Not public",
            is_published=False,
        )

        response = self.client.get(
            reverse("information_page", args=[page.slug])
        )

        self.assertEqual(response.status_code, 404)

    def test_active_teacher_has_a_public_profile(self):
        teacher = Teacher.objects.create(
            name="Asha Sharma",
            designation="Teacher",
            subject="Science",
            qualification="M.Sc.",
            description="Teacher profile",
        )

        response = self.client.get(
            reverse("teacher_detail", args=[teacher.pk])
        )

        self.assertContains(response, teacher.name)
        self.assertContains(response, teacher.qualification)

    def test_homepage_uses_admin_managed_hero_text(self):
        SiteSettings.objects.create(hero_heading="A dynamic college heading")

        response = self.client.get(reverse("home"))

        self.assertContains(response, "A dynamic college heading")

    def test_language_switch_rejects_external_redirect(self):
        response = self.client.post(
            reverse("switch_language"),
            {"language": "hi", "next": "https://example.com/"},
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.session["site_language"], "hi")

    def test_admission_form_labels_follow_selected_language(self):
        response = self.client.post(
            reverse("switch_language"),
            {"language": "hi", "next": reverse("admission_enquiry")},
        )
        self.assertRedirects(response, reverse("admission_enquiry"))

        page = self.client.get(reverse("admission_enquiry"))

        self.assertContains(page, "विद्यार्थी का नाम")
        self.assertContains(page, 'lang="hi"')

    def test_staff_with_permission_can_update_admission_status(self):
        staff_user = User.objects.create_user(
            username="admission-handler",
            password="Strong-Test-Password-927!",
            is_staff=True,
        )
        permissions = Permission.objects.filter(
            content_type__app_label="website",
            codename__in=(
                "view_admissionenquiry",
                "change_admissionenquiry",
            ),
        )
        staff_user.user_permissions.add(*permissions)
        enquiry = AdmissionEnquiry.objects.create(
            student_name="Student Example",
            father_name="Parent Example",
            class_applying_for="9",
            mobile="9876543210",
            address="College road",
        )
        self.client.force_login(staff_user)

        response = self.client.post(
            reverse("update_admission_status", args=[enquiry.pk]),
            {"status": AdmissionEnquiry.Status.CONTACTED, "internal_notes": "Called"},
        )

        enquiry.refresh_from_db()
        self.assertRedirects(response, reverse("staff_admissions"))
        self.assertEqual(enquiry.status, AdmissionEnquiry.Status.CONTACTED)
        self.assertEqual(enquiry.internal_notes, "Called")

    def test_staff_without_admission_permission_cannot_open_queue(self):
        staff_user = User.objects.create_user(
            username="basic-staff",
            password="Strong-Test-Password-927!",
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse("staff_admissions"))

        self.assertEqual(response.status_code, 403)

    def test_staff_queues_render_for_users_with_model_permissions(self):
        staff_user = User.objects.create_user(
            username="office-staff",
            password="Strong-Test-Password-927!",
            is_staff=True,
        )
        permissions = Permission.objects.filter(
            content_type__app_label="website",
            codename__in=(
                "view_admissionenquiry",
                "view_contactmessage",
            ),
        )
        staff_user.user_permissions.add(*permissions)
        AdmissionEnquiry.objects.create(
            student_name="Student Example",
            father_name="Parent Example",
            class_applying_for="9",
            mobile="9876543210",
            address="College road",
        )
        ContactMessage.objects.create(
            name="Parent Example",
            email="parent@example.com",
            subject="Question",
            message="Please call me back.",
        )
        self.client.force_login(staff_user)

        admissions_response = self.client.get(reverse("staff_admissions"))
        messages_response = self.client.get(reverse("staff_messages"))

        self.assertEqual(admissions_response.status_code, 200)
        self.assertContains(admissions_response, "Student Example")
        self.assertEqual(messages_response.status_code, 200)
        self.assertContains(messages_response, "Please call me back.")

    @override_settings(
        COLLEGE_NOTIFICATION_EMAIL="college@example.com",
        DEFAULT_FROM_EMAIL="website@example.com",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_admission_submission_sends_staff_email(self):
        response = self.client.post(reverse("admission_enquiry"), {
            "student_name": "Student Example",
            "father_name": "Parent Example",
            "class_applying_for": "9",
            "mobile": "9876543210",
            "email": "parent@example.com",
            "address": "College road",
        })

        self.assertRedirects(response, reverse("admission_enquiry"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["college@example.com"])
