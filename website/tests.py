from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class PublicPageTests(TestCase):
    def test_admission_links_use_the_enquiry_page(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            f'href="{reverse("admission_enquiry")}" class="nav-btn"',
        )
        self.assertContains(
            response,
            f'<li><a href="{reverse("admission_enquiry")}">Admission Enquiry</a></li>',
        )

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
