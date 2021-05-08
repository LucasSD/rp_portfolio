import time
from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Category, Comment

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
            # this delay ensures the context created in the relvant view is not ordered randomly
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

        # check the number of blog posts is correct
        self.assertTrue(len(response.context["posts"]) == 5)

    def test_context(self):
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)

        # loop in order of "created_on," but in ascending 
        #TODO add test for ManyToMany field in context
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
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/blog/<category>/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self): # this currently produces an error
        response = self.client.get(reverse("blog_category"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get("/blog/<category>/")
        #response = self.client.get(reverse("blog_category"))
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
            # this delay ensures the context created in the relvant view is not ordered randomly
            time.sleep(0.0001) 

        
        for comment_author in authors:
            Comment.objects.create(
            author=comment_author,
            body = "blah blah",
            post = Post.objects.get(id=1),
            )

    def test_view_url_exists_at_desired_location(self):
        # for all instances in the test database
        for i in Post.objects.all():
            response = self.client.get(f"/blog/{i.id}/")
        #response = self.client.get("/blog/<int:pk>/") - what exactly is happening with this test?
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self): # this causes an error currently
        response = self.client.get(reverse("blog_detail"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for blog_post in Post.objects.all():
            response = self.client.get(f"/blog/{blog_post.id}/")
        #response = self.client.get(reverse("blog_category"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_displays_one_blog_post(self):
        for blog_post in Post.objects.all():
            response = self.client.get(f"/blog/{blog_post.id}/")
            #response = self.client.get(reverse("blog_detail"))
            self.assertEqual(response.status_code, 200)

            # need to make it an iterable to check the length
            self.assertTrue(len([response.context["post"]]) == 1)

    def test_post_context(self):
        for blog_post in Post.objects.all():
            response = self.client.get(f"/blog/{blog_post.id}/")
            #response = self.client.get(reverse("blog_detail"))
            self.assertEqual(response.status_code, 200)

            blog_post = response.context["post"]
            self.assertEqual(f"Blog Post {blog_post.id - 1}", blog_post.title)
            self.assertEqual("This is the body...", blog_post.body)
            self.assertIsInstance(blog_post.created_on, datetime)
            self.assertIsInstance(blog_post.last_modified, datetime)
            self.assertEqual("https://cscircles.cemc.uwaterloo.ca/", blog_post.link)

    def test_displays_all_comments(self):
        blog_post = Post.objects.get(id=1) # this blog post has three comments
        response = self.client.get(f"/blog/{blog_post.id}/")
        #response = self.client.get(reverse("blog_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["comments"]) == 3)

    def test_displays_no_comments(self):
        blog_post = Post.objects.get(id=2) # this blog post has no comments
        response = self.client.get(f"/blog/{blog_post.id}/")
        #response = self.client.get(reverse("blog_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["comments"]) == 0)

    def test_comments_context(self):
        response = self.client.get("/blog/1/")
        self.assertEqual(response.status_code, 200)
        #response = self.client.get(reverse("blog_detail"))
        for comment, author in zip(response.context["comments"], authors):
            self.assertEqual(author, comment.author)
            self.assertEqual("blah blah", comment.body)
            self.assertIsInstance(comment.created_on, datetime)
            self.assertEqual("Blog Post 0", str(comment.post))


    


