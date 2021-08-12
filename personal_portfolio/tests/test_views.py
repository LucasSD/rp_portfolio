from django.test import TestCase
from django.urls import reverse

class CvViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cv/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("cv"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("cv"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cv.html")
        self.assertTemplateUsed(response, "base.html")