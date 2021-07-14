from django.test import TestCase

from projects.models import Project


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(
            title="Web Scraper",
            description="This scrapes websites.",
            summary="This scrapes...",
            technology="scrapy",
            image="img/JL.png",
            repo="https://github.com/LucasSD/web-scraping",
        )

    def test_title_max_length(self):
        p = Project.objects.get(id=1)
        max_length = p._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_summary_max_length(self):
        p = Project.objects.get(id=1)
        max_length = p._meta.get_field("summary").max_length
        self.assertEqual(max_length, 100)

    def test_technology_max_length(self):
        p = Project.objects.get(id=1)
        max_length = p._meta.get_field("technology").max_length
        self.assertEqual(max_length, 100)

    def test_image_max_length(self):
        p = Project.objects.get(id=1)
        max_length = p._meta.get_field("image").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_project_title(self):
        p = Project.objects.get(id=1)
        expected_object_name = f"{p.title}"
        self.assertEqual(expected_object_name, str(p))
