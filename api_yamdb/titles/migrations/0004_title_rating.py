# Generated by Django 2.2.16 on 2021-10-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0003_auto_20211014_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.PositiveIntegerField(default=0, verbose_name='Рейтинг'),
            preserve_default=False,
        ),
    ]
