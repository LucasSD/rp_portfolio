# Generated by Django 3.1.7 on 2021-03-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20210325_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='summary',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.FilePathField(path='C:\\Users\\Haamiyah\\Desktop\\Lucas\\Python Stuff\\rp_portfolio\\projects\\static\\img'),
        ),
    ]
