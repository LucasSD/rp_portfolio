# Generated by Django 3.1.7 on 2021-03-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210324_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='repo',
            field=models.URLField(default='to be entered in admin'),
            preserve_default=False,
        ),
    ]
