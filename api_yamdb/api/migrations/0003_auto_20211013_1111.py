# Generated by Django 2.2.16 on 2021-10-13 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211013_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='category',
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Title',
        ),
    ]