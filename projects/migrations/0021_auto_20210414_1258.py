# Generated by Django 2.2.7 on 2021-04-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20210414_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.FilePathField(path='./static/img'),
        ),
    ]
