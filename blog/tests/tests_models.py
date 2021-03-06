from datetime import datetime

from blog.models import Category, Comment, Post
from django.test import TestCase


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="Resources")

    def test_name_max_length(self):
        c = Category.objects.get(id=1)
        max_length = c._meta.get_field("name").max_length
        self.assertEqual(max_length, 21)

    def test_object_name_is_category_name(self):  # test __str__
        c = Category.objects.get(id=1)
        expected_object_name = f"{c.name}"
        self.assertEqual(expected_object_name, str(c))


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Post.objects.create(title="test blog")

        Comment.objects.create(
            author="Lucas",
            post=p,
        )

    def test_author_max_length(self):
        c = Comment.objects.get(id=1)
        max_length = c._meta.get_field("author").max_length
        self.assertEqual(max_length, 60)

    def test_post_field(self):
        c = Comment.objects.get(id=1)
        expected_post = c.post
        self.assertEqual(str(expected_post), "test blog")

    def test_object_name_is_comment_author(self):  # test __str__
        c = Comment.objects.get(id=1)
        expected_object_name = f"{c.author}"
        self.assertEqual(expected_object_name, str(c))


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cat = Category.objects.create(name="Test Category")

        p = Post.objects.create(
            title="This is a great blog post",
        )

    def test_title_max_length(self):
        p = Post.objects.get(id=1)
        max_length = p._meta.get_field("title").max_length
        self.assertEqual(max_length, 255)

    def test_categories_field(self):
        cat = Category.objects.get(id=1)
        cat.save()

        p = Post.objects.get(id=1)
        p.categories.add(cat)
        p.save()
        expected_category = str(
            p.categories.all()[0]
        )  # queryset is a list of length one
        self.assertEqual(expected_category, "Test Category")

    def test_object_name_is_post_title(self):  # test __str__
        c = Post.objects.get(id=1)
        expected_object_name = f"{c.title}"
        self.assertEqual(expected_object_name, str(c))
