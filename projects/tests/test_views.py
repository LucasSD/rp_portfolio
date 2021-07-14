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
                order=p
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

        for i, project in enumerate(response.context["projects"]):
            self.assertEqual("scrapy", project.technology)
            self.assertEqual("img/JL.png", project.image)
            self.assertEqual("https://github.com/LucasSD/web-scraping", project.repo)
            self.assertEqual("This scrapes...", project.summary)
            self.assertEqual("This scrapes websites.", project.description)
            self.assertEqual(f"Web Scraper {i}", project.title)

    def test_project_order(self):
        Project.objects.create(
                title=f"First Project",
                description="This scrapes websites.",
                summary="This scrapes...",
                technology="scrapy",
                image="img/JL.png",
                repo="https://github.com/LucasSD/web-scraping",
                order=-4
            )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        first_project = response.context["projects"][0]
        third_project = response.context["projects"][2]
        self.assertEqual("First Project", first_project.title)
        self.assertEqual("Web Scraper 1", third_project.title)
        


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

    def test_view_url_accessible_by_name(self):
        for project in Project.objects.all():
            response = self.client.get(
                reverse("project_detail", kwargs={"pk": project.id})
            )
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get("/2/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_displays_one_project(self):
        for project in Project.objects.all():
            response = self.client.get(
                reverse("project_detail", kwargs={"pk": project.id})
            )
            self.assertEqual(response.status_code, 200)

            # need to make it an iterable to check the length
            self.assertTrue(len([response.context["project"]]) == 1)

    def test_context(self):
        for project in Project.objects.all():
            response = self.client.get(
                reverse("project_detail", kwargs={"pk": project.id})
            )
            self.assertEqual(response.status_code, 200)

            self.assertEqual("scrapy", project.technology)
            self.assertEqual("img/JL.png", project.image)
            self.assertEqual("https://github.com/LucasSD/web-scraping", project.repo)
            self.assertEqual("This scrapes...", project.summary)
            self.assertEqual("This scrapes websites.", project.description)
            self.assertEqual(f"Web Scraper {project.id - 1}", project.title)

