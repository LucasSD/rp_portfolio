# Generated by Django 3.1.7 on 2021-06-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20210414_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='technology',
            field=models.CharField(max_length=100),
        ),
    ]
