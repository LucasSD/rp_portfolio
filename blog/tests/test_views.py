import time
from datetime import datetime

from blog.forms import CommentForm
from blog.models import Category, Comment, Post
from django.test import TestCase
from django.urls import reverse

authors = ["Lucas", "James", "Haamiyah"]


class BlogIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 5

        for blog_post in range(number_of_posts):
            Post.objects.create(
                title=f"Blog Post {blog_post}",
                body="This is the body...",
                link="https://cscircles.cemc.uwaterloo.ca/",
            )
            # this delay ensures the db is not ordered randomly
            time.sleep(0.0001)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog_index.html")
        self.assertTemplateUsed(response, "base.html")

    def test_displays_all_posts(self):
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)

        # check the number of blog posts
        self.assertTrue(len(response.context["posts"]) == 5)

    def test_context(self):
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)

        # loop in order of "created_on"
        # TODO add test for ManyToMany field in context
        for i, post in enumerate(response.context["posts"].order_by("created_on")):
            self.assertEqual(f"Blog Post {i}", post.title)
            self.assertEqual("This is the body...", post.body)
            self.assertIsInstance(post.created_on, datetime)
            self.assertIsInstance(post.last_modified, datetime)
            self.assertEqual("https://cscircles.cemc.uwaterloo.ca/", post.link)


class BlogCategoryViewTest(TestCase):
    @classmethod
    # Need a set-up which can handle the ManyToMany field Post.categories
    def setUpTestData(cls):
        cat = Category.objects.create(name="Test-Category")

    def test_view_url_exists_at_desired_location(self):
        cat = Category.objects.get(id=1)
        response = self.client.get(f"/blog/{cat.name}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        cat = Category.objects.get(id=1)
        response = self.client.get(reverse("blog_category", kwargs={"category": cat}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        cat = Category.objects.get(id=1)
        response = self.client.get(reverse("blog_category", kwargs={"category": cat}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog_category.html")
        self.assertTemplateUsed(response, "base.html")


class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 5

        for blog_post in range(number_of_posts):
            Post.objects.create(
                title=f"Blog Post {blog_post}",
                body="This is the body...",
                link="https://cscircles.cemc.uwaterloo.ca/",
            )
            # this delay ensures the db is not ordered randomly
            time.sleep(0.0001)

            form = CommentForm()

        for comment_author in authors:
            Comment.objects.create(
                author=comment_author,
                body="blah blah",
                post=Post.objects.get(id=1),
            )

    def test_view_url_exists_at_desired_location(self):
        for blog_post in Post.objects.all():
            response = self.client.get(f"/blog/{blog_post.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for blog_post in Post.objects.all():
            response = self.client.get(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for blog_post in Post.objects.all():
            response = self.client.get(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_displays_one_blog_post(self):
        for blog_post in Post.objects.all():
            response = self.client.get(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
            self.assertEqual(response.status_code, 200)

            # need to make post context an iterable to check the length
            self.assertTrue(len([response.context["post"]]) == 1)

    def test_post_context(self):
        for blog_post in Post.objects.all():
            response = self.client.get(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
            self.assertEqual(response.status_code, 200)

            blog_post = response.context["post"]
            self.assertEqual(f"Blog Post {blog_post.id - 1}", blog_post.title)
            self.assertEqual("This is the body...", blog_post.body)
            self.assertIsInstance(blog_post.created_on, datetime)
            self.assertIsInstance(blog_post.last_modified, datetime)
            self.assertEqual("https://cscircles.cemc.uwaterloo.ca/", blog_post.link)

    def test_displays_all_comments(self):
        blog_post = Post.objects.get(id=1)  # this blog post has three comments
        response = self.client.get(reverse("blog_detail", kwargs={"pk": blog_post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["comments"]) == 3)

    def test_displays_no_comments(self):
        blog_post = Post.objects.get(id=2)  # this blog post has no comments
        response = self.client.get(reverse("blog_detail", kwargs={"pk": blog_post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["comments"]) == 0)

    def test_comments_context(self):
        response = self.client.get(reverse("blog_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        for comment, author in zip(response.context["comments"], authors):
            self.assertEqual(author, comment.author)
            self.assertEqual("blah blah", comment.body)
            self.assertIsInstance(comment.created_on, datetime)
            self.assertEqual("Blog Post 0", str(comment.post))

    def test_form_context(self):
        for blog_post in Post.objects.all():
            response = self.client.get(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
            self.assertEqual(response.status_code, 200)

            form = response.context["form"]
            self.assertIn("form", response.context)
            self.assertEqual({}, form.initial)
            self.assertEqual(None, form["author"].value())
            self.assertEqual(None, form["body"].value())

    def test_redirects_to_same_page_when_comment_submitted(self):
        for blog_post in Post.objects.all():
            response = self.client.post(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
            request = self.client.get(
                reverse("blog_detail", kwargs={"pk": blog_post.id})
            )
            self.assertURLEqual(response, request)

    def test_comment_form(self):
        blog_post = Post.objects.get(id=3)
        form_entry = {
            "author": "Formy",
            "body": "Test this comment form",
            "post": blog_post,
        }

        response = self.client.post(
            reverse("blog_detail", kwargs={"pk": 3}), data=form_entry
        )
        comment = Comment.objects.get(id=4)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 4)
        self.assertEqual("Formy", comment.author)
        self.assertEqual("Test this comment form", comment.body)
        self.assertIsInstance(comment.created_on, datetime)
        self.assertEqual("Blog Post 2", str(comment.post))
