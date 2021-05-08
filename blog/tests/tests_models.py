from datetime import datetime

from django.test import TestCase

from blog.models import Post, Comment, Category

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='Resources')

    def test_name_max_length(self):
        c = Category.objects.get(id=1)
        max_length = c._meta.get_field("name").max_length
        self.assertEqual(max_length, 21)

    def test_object_name_is_category_name(self): # test __str__
        c = Category.objects.get(id=1)
        expected_object_name = f"{c.name}"
        self.assertEqual(expected_object_name, str(c))

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        p = Post.objects.create(
            title = "test blog"
        )
        
        Comment.objects.create(
            author="Lucas",
            post = p,
        )

    def test_author_max_length(self):
        c = Comment.objects.get(id=1)
        max_length = c._meta.get_field("author").max_length
        self.assertEqual(max_length, 60)

    def test_post_field(self): # test ForeignKey Field
        c = Comment.objects.get(id=1)
        expected_post = c.post
        self.assertEqual(str(expected_post), "test blog")

    def test_object_name_is_comment_author(self): # test __str__
        c = Comment.objects.get(id=1)
        expected_object_name = f"{c.author}"
        self.assertEqual(expected_object_name, str(c))

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        
        cat = Category.objects.create(
            name = "Test Category"
        )
        
        p = Post.objects.create(
            title="This is a great blog post",
        )
        

    def test_title_max_length(self):
        p = Post.objects.get(id=1)
        max_length = p._meta.get_field("title").max_length
        self.assertEqual(max_length, 255)

        #need to read https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/ to get below to work

    def test_categories_field(self): # Test ManyToManyField - this currently causes an error
        p = Post.objects.get(id=1)
        expected_category = p.categories
        self.assertEqual(str(expected_category), "Test Category")

    def test_object_name_is_post_title(self): # test __str__
        c = Post.objects.get(id=1)
        expected_object_name = f"{c.title}"
        self.assertEqual(expected_object_name, str(c))
    