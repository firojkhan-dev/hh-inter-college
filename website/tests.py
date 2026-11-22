from django.test import TestCase
from django.urls import reverse


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
        response = self.client.post(
            reverse("home"),
            {
                "name": "x",
                "email": "invalid",
                "phone": "",
                "subject": "",
                "message": "short",
            },
        )

        self.assertContains(response, 'class="error-message"')
        self.assertNotContains(response, 'class="success-message"')

    def test_invalid_admission_submission_is_not_styled_as_success(self):
        response = self.client.post(reverse("admission_enquiry"), {})

        self.assertContains(response, 'class="alert alert-error"')
        self.assertNotContains(response, 'class="alert alert-success"')
