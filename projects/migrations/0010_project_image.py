# Generated by Django 2.2.7 on 2021-04-13 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_remove_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.FilePathField(default='selectimage', path='projects/static/img'),
            preserve_default=False,
        ),
    ]
