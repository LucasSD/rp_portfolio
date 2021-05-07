from django.test import TestCase
from django.urls import reverse

from projects.models import Project


class ProjectIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create five projects in database. This data cannot be modified.
        number_of_projects = 5

        for p in range(number_of_projects):
            Project.objects.create(
                title=f"Web Scraper {p}",
                description="This scrapes websites.",
                summary="This scrapes...",
                technology="scrapy",
                image="img/JL.png",
                repo="https://github.com/LucasSD/web-scraping",
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_index.html")
        self.assertTemplateUsed(response, "base.html")

    def test_displays_all_projects(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        # check the number of projects is correct
        self.assertTrue(len(response.context["projects"]) == 5)

    def test_context(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        for i, p in enumerate(response.context["projects"]):
            self.assertEqual("scrapy", p.technology)
            self.assertEqual("img/JL.png", p.image)
            self.assertEqual("https://github.com/LucasSD/web-scraping", p.repo)
            self.assertEqual("This scrapes...", p.summary)
            self.assertEqual("This scrapes websites.", p.description)
            self.assertEqual(f"Web Scraper {i}", p.title)


class ProjectDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create five projects
        number_of_projects = 5

        for p in range(number_of_projects):
            Project.objects.create(
                title=f"Web Scraper {p}",
                description="This scrapes websites.",
                summary="This scrapes...",
                technology="scrapy",
                image="img/JL.png",
                repo="https://github.com/LucasSD/web-scraping",
            )

    def test_view_url_exists_at_desired_location(self):
        # for all instances in the test database
        for i in Project.objects.all():
            response = self.client.get(f"/{i.id}/")
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self, pk):
        for i in Project.objects.all():
            self.pk = i.id
            response = self.client.get(reverse("project_detail"))
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get("/2/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")
        self.assertTemplateUsed(response, "base.html")
