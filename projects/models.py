from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    summary = models.CharField(max_length=100)
    technology = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    repo = models.URLField()

    def __str__(self):
        return self.title
